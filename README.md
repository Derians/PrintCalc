# PrintCalc

*English* | *[Русский](#русский)*

Web application for calculating 3D printing costs, supporting both FDM and resin printing.

![License](https://img.shields.io/github/license/Derians/PrintCalc)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Version](https://img.shields.io/github/v/tag/Derians/PrintCalc)

## Features
- FDM and resin printing cost calculation
- Material and electricity cost tracking
- Material database with weight and price
- Customizable markup multiplier
- English and Russian interface
- RESTful API for integration
- Git-based versioning

## Screenshots
(Add your screenshots here)

## Requirements
- Python 3.8 or higher
- Dependencies from requirements.txt

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PrintCalc.git
cd PrintCalc
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

4. Run the application:
```bash
# Development
python wsgi.py

# Production (Windows Service)
install_service_windows.bat  # Run as Administrator

# Production (Linux Service)
sudo ./install_service.sh
```

Access the calculator at `http://localhost:5000`

## Development

### Project Structure
```
PrintCalc/
├── printcalc/         # Main package
│   ├── __init__.py   # Application factory
│   ├── config.py     # Configuration
│   ├── db.py        # Database operations
│   ├── routes.py    # Route handlers
│   ├── static/      # Static files (CSS)
│   └── templates/   # HTML templates
├── init_db.py       # Database initialization
├── wsgi.py         # WSGI entry point
└── requirements.txt # Dependencies
```

### Application Architecture

PrintCalc is built using Flask and follows the application factory pattern. Key components:

- `printcalc/__init__.py`: Application factory that creates and configures the Flask app
- `printcalc/config.py`: Configuration settings (database, logging, etc.)
- `printcalc/db.py`: SQLite database operations
- `printcalc/routes.py`: Route handlers and business logic

The application uses SQLite for data storage and Waitress as the WSGI server in production.

### API Reference

PrintCalc provides a simple web interface and can be integrated with other applications through its HTTP endpoints:

#### Calculate Print Cost

```http
POST /calculate
Content-Type: application/json

{
    "spool_id": 1,
    "weight": 15.5,
    "time_hours": 4.0,
    "print_type": "filament"  // or "resin"
}
```

Response:
```json
{
    "cost": 2.50,
    "currency": "EUR"
}
```

#### Material Management

Get all materials:
```http
GET /api/spools
```

Add new material:
```http
POST /api/spools
Content-Type: application/json

{
    "name": "PLA White",
    "weight": 1000,
    "price": 25.0,
    "type": "filament"
}
```

Update material:
```http
PUT /api/spools/{id}
Content-Type: application/json

{
    "name": "PLA White",
    "weight": 1000,
    "price": 23.0
}
```

Delete material:
```http
DELETE /api/spools/{id}
```

#### Settings

Get current settings:
```http
GET /api/settings
```

Update settings:
```http
PUT /api/settings
Content-Type: application/json

{
    "energy_price": 0.15,
    "power_watt": 350,
    "markup_multiplier": 1.5
}
```

### Contributing
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# Русский

Веб-приложение для расчёта стоимости 3D печати с поддержкой FDM и смолы.

## Возможности
- Расчёт стоимости для FDM и смоляной печати
- Учёт стоимости материалов и электроэнергии
- База данных материалов с весом и ценой
- Настраиваемый множитель наценки
- Интерфейс на русском и английском языках
- REST API для интеграции
- Версионирование на основе git

## Требования
- Python 3.8 или выше
- Зависимости из requirements.txt

## Быстрый старт

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/PrintCalc.git
cd PrintCalc
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Инициализируйте базу данных:
```bash
python init_db.py
```

4. Запустите приложение:
```bash
# Разработка
python wsgi.py

# Установка как службы Windows
install_service_windows.bat  # Запуск от имени администратора

# Установка как службы Linux
sudo ./install_service.sh
```

Калькулятор будет доступен по адресу `http://localhost:5000`

## Разработка

### Структура проекта
```
PrintCalc/
├── printcalc/         # Основной пакет
│   ├── __init__.py   # Фабрика приложения
│   ├── config.py     # Конфигурация
│   ├── db.py        # Операции с БД
│   ├── routes.py    # Обработчики маршрутов
│   ├── static/      # Статические файлы (CSS)
│   └── templates/   # HTML шаблоны
├── init_db.py       # Инициализация БД
├── wsgi.py         # Точка входа WSGI
└── requirements.txt # Зависимости
```

### Архитектура приложения

PrintCalc построен на Flask и использует паттерн фабрики приложения. Основные компоненты:

- `printcalc/__init__.py`: Фабрика приложения, создающая и настраивающая Flask-приложение
- `printcalc/config.py`: Настройки (база данных, логирование и т.д.)
- `printcalc/db.py`: Операции с SQLite базой данных
- `printcalc/routes.py`: Обработчики маршрутов и бизнес-логика

Приложение использует SQLite для хранения данных и Waitress как WSGI-сервер в продакшене.

### Справка по API

PrintCalc предоставляет веб-интерфейс и может быть интегрирован с другими приложениями через HTTP-эндпоинты:

#### Расчёт стоимости печати

```http
POST /calculate
Content-Type: application/json

{
    "spool_id": 1,
    "weight": 15.5,
    "time_hours": 4.0,
    "print_type": "filament"  // или "resin"
}
```

Ответ:
```json
{
    "cost": 2.50,
    "currency": "EUR"
}
```

#### Управление материалами

Получить все материалы:
```http
GET /api/spools
```

Добавить материал:
```http
POST /api/spools
Content-Type: application/json

{
    "name": "PLA White",
    "weight": 1000,
    "price": 25.0,
    "type": "filament"
}
```

Обновить материал:
```http
PUT /api/spools/{id}
Content-Type: application/json

{
    "name": "PLA White",
    "weight": 1000,
    "price": 23.0
}
```

Удалить материал:
```http
DELETE /api/spools/{id}
```

#### Настройки

Получить текущие настройки:
```http
GET /api/settings
```

Обновить настройки:
```
