from flask import Flask
import logging
import os
from . import config
from . import db

def create_app():
    app = Flask(__name__)
    
    # Apply settings from config
    app.config['VERSION'] = config.VERSION
    app.config['DATABASE'] = config.DATABASE
    app.config['DEBUG'] = config.DEBUG
    app.config['SECRET_KEY'] = config.SECRET_KEY
    
    # Setup logging
    log_dir = os.path.dirname(config.LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logging.basicConfig(
        filename=config.LOG_FILE,
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Register routes
    from .routes import register_routes
    register_routes(app)
    
    return app