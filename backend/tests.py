import os
import tempfile
import pytest
from app import app
from flask import request, jsonify


@pytest.fixture
def client():
    app.reque
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_about_get(client):
    """Start with a blank database."""

    rv = client.get('/about')
    assert b'This is the backend of EventIT' in rv.data

def test_create_user(client):
    """It should be possible to create a user"""

    res = client.post('/users', json={})

    assert b'"_status": "OK"' in res.data

def test_create_ruleset(client):
    """It should be possible to define a ruleset"""

    res = client.post('/location-rulesets', json={
        [

        ]
    })

    print(res)


def test_create_location(client):
    """It should be possible to add a new location to the database."""

    res = client.post('/locations', json={
        "name": "Hubben 2.1",
        "address": "Hörsalsvägen 9, 412 58 Göteborg",
        "description": "An awesome place for awesome people!",
        "coordinate": {
            "type": "Point",
            "coordinates": [
                57.688348,
                11.979196
            ]
        }})

    print(res)
