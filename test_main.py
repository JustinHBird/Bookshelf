import os
import pytest
import requests
from flask import url_for
import main

@pytest.fixture
def app(request):
    """This fixture provides a Flask app instance configured for testing.

    It uses the test_request_context() method to ensures the tests run with a request context, 
    allowing any calls to flask.request, flask.current_app, etc. to work.
    For more infor on test_request_context():
        https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.test_request_context"""
    app = main.app

    with app.test_request_context():
        yield app

def test_hello(app):
    response = app.test_client().get(url_for('hello'))
    assert response.status_code == 200
    assert response.data == b'Hello, World'

def test_index(app):
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'This is the index'