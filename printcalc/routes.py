from flask import render_template, request, redirect, url_for, make_response, Flask
import logging
from . import db
from .translations import LANGUAGES
from .config import VERSION, FULL_VERSION

def get_translation():
    lang = request.cookies.get("lang")
    if lang in LANGUAGES:
        return LANGUAGES[lang], lang

    accept = request.headers.get("Accept-Language", "").lower()
    for code in LANGUAGES:
        if code in accept:
            return LANGUAGES[code], code

    return LANGUAGES["en"], "en"

def register_routes(app):
    @app.route('/set_lang/<lang_code>')
    def set_lang(lang_code):
        if lang_code not in LANGUAGES:
            lang_code = "en"
        logging.info(f"Setting language to: {lang_code}")
        resp = make_response(redirect(request.referrer or url_for('index')))
        # Set cookie for 1 year
        resp.set_cookie("lang", lang_code, max_age=60 * 60 * 24 * 365)
        return resp

    @app.route('/', methods=['GET', 'POST'])
    def index():
        t, lang = get_translation()
        result = None
        print_type = request.form.get('print_type', 'filament')
        spools = db.get_spools()
        energy_price = db.get_config('energy_price')
        power_watt = db.get_config('power_watt')
        markup = db.get_config('markup_multiplier')

        if request.method == 'POST':
            try:
                spool_id = int(request.form['spool'])
                part_weight = float(request.form['part_weight'])
                time_hours = float(request.form.get('time_hours') or 0)

                spool = db.get_spool(spool_id)
                logging.info(f"Calculating cost for spool_id={spool_id}, weight={part_weight}g, time={time_hours}h")

                if print_type == "resin":
                    cost_per_gram = spool['price'] / spool['weight']
                    total = round(cost_per_gram * part_weight * markup, 2)
                else:
                    cost_per_gram = spool['price'] / spool['weight']
                    plastic_cost = cost_per_gram * part_weight
                    power_kw = power_watt / 1000
                    energy_cost = power_kw * time_hours * energy_price
                    total = round((plastic_cost + energy_cost) * markup, 2)

                result = f"{total} €"
                logging.info(f"Calculated cost: {result}")
            except Exception as e:
                logging.error(f"Error calculating cost: {e}")
                result = f"Error: {e}"

        return render_template('index.html',
                             spools=spools,
                             result=result,
                             energy_price=energy_price,
                             power_watt=power_watt,
                             t=t,
                             lang=lang,
                             version=VERSION)

    @app.route('/settings', methods=['GET', 'POST'])
    def settings():
        t, lang = get_translation()

        if request.method == 'POST':
            if 'add_spool' in request.form:
                name = request.form['name']
                weight = float(request.form['weight'])
                price = float(request.form['price'])
                spool_type = request.form.get('type', 'filament')
                logging.info(f"Adding new spool: {name} ({weight}g, {price}€, type={spool_type})")
                db.add_spool(name, weight, price, spool_type)
            elif 'update_energy' in request.form:
                price = float(request.form['energy_price'])
                logging.info(f"Updating energy price to: {price}€/kWh")
                db.update_config('energy_price', price)
            elif 'update_power' in request.form:
                power = float(request.form['power_watt'])
                logging.info(f"Updating power consumption to: {power}W")
                db.update_config('power_watt', power)
            elif 'update_markup' in request.form:
                markup = float(request.form['markup_multiplier'])
                logging.info(f"Updating markup multiplier to: {markup}")
                db.update_config('markup_multiplier', markup)

            return redirect(url_for('settings', lang=lang))

        spools = db.get_spools()
        current_price = db.get_config('energy_price')
        current_power = db.get_config('power_watt')
        markup = db.get_config('markup_multiplier')
        return render_template('settings.html',
                             spools=spools,
                             current_price=current_price,
                             current_power=current_power,
                             markup=markup,
                             t=t,
                             lang=lang,
                             version=VERSION)

    @app.route('/edit_spool/<int:spool_id>', methods=['GET', 'POST'])
    def edit_spool(spool_id):
        t, lang = get_translation()
        spool = db.get_spool(spool_id)
        if request.method == 'POST':
            name = request.form['name']
            weight = float(request.form['weight'])
            price = float(request.form['price'])
            db.update_spool(spool_id, name, weight, price)
            return redirect(url_for('settings', lang=lang))
        return render_template('edit_spool.html', spool=spool, t=t, lang=lang)

    @app.route('/delete_spool/<int:spool_id>', methods=['POST'])
    def delete_spool(spool_id):
        t, lang = get_translation()
        db.delete_spool(spool_id)
        return redirect(url_for('settings', lang=lang))