import pytest
from flask import Flask
from flask.testing import FlaskClient
from controllers.accidents_controller import accidents_blueprint  # כאן תוודא שאתה שם את הנתיב הנכון למודול של הבקר

@pytest.fixture
def app() -> Flask:
    """ הגדרת Flask עבור סביבת בדיקות """
    app = Flask(__name__)
    app.register_blueprint(accidents_blueprint, url_prefix="/api/accidents")
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_initialize_db(client: FlaskClient):
    response = client.post('/api/accidents/initialize-db')
    assert response.status_code == 200
    assert response.json['message'] == 'Database initialized successfully'


def test_total_accidents_in_area(client: FlaskClient):
    area = 225
    response = client.get(f'/api/accidents/{area}')
    assert response.status_code == 200
    assert isinstance(response.json['body'], list)


def test_get_accidents_by_area(client: FlaskClient):
    area = 225
    time_type = 'd'
    date = '2023-10-01'
    response = client.get(f'/api/accidents/accidents_by_date/{area}?time-type={time_type}&date={date}')
    assert response.status_code == 200
    assert 'body' in response.json


def test_accidents_by_cause(client: FlaskClient):
    area = 225
    response = client.get(f'/api/accidents/by_cause/{area}')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_injury_stats_by_area(client: FlaskClient):
    area = 225
    response = client.get(f'/api/accidents/injury_stats/{area}')
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert 'total_injuries' in response.json
    assert 'fatal_injuries' in response.json
    assert 'non_fatal_injuries' in response.json
