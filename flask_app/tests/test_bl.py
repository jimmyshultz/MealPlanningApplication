
"""
    A class to test the DAL class methods.

    Some tests use the test data that is included in the database 
    creation scripts.

    Attributes
    ----------
    dal : DAL
        An instance of the DAL class.
    
    Tested Methods
    --------------
    
    Untested Methods
    ----------------
    - check_recipe - not implemented
    - get_cookbook_names - 
    - get_cookbook_info - 
    - get_recipe_names - 
    - get_all_recipe_names - 
    - get_recipe_info - 
    - add_cookbook - 
    - delete_cookbook - 
    - add_recipe - 
    - delete_recipe - 
    - add_ingredient - 
    - delete_ingredient - 
    - add_ingredient_recipe_pairing - 
    - add_user - 
    - login_user - 
    
"""

import pytest, sys, os
from unittest.mock import MagicMock
from flask import Flask, session, jsonify

# Add the backend directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from meal_planning_backend import DAL, BusinessLogic

@pytest.fixture
def dal_mock():
    """Fixture to mock the Data Access Layer."""
    mock = MagicMock()
    mock.get_recipe_names.return_value = ['recipe1', 'recipe2']
    mock.get_cookbook_names.return_value = ['cookbook1', 'cookbook2']
    mock.get_cookbook_info.return_value = ('Cookbook1', 1, 'http://example.com')
    return mock

@pytest.fixture
def app(dal_mock):
    """Fixture to create the Flask app with a mocked DAL."""
    business_logic = BusinessLogic(dal_mock)
    business_logic.app.config['TESTING'] = True
    business_logic.app.config['SECRET_KEY'] = 'test'
    with business_logic.app.test_client() as client:
        with business_logic.app.app_context():
            yield client

class TestBL:

    @pytest.fixture(autouse=True)
    def setup(self, app, dal_mock):
        """Setup for each test method."""
        self.app = app
        self.dal_mock = dal_mock

    def test_check_recipe_valid(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/check_recipe/recipe1')
        assert response.status_code == 200
        assert response.json == {'validity': True}

    def test_check_recipe_invalid(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/check_recipe/invalid_recipe')
        assert response.status_code == 200
        assert response.json == {'validity': False}

    def test_get_cookbook_names(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/cookbook_names')
        assert response.status_code == 200
        assert response.json == ['cookbook1', 'cookbook2']

    def test_get_cookbook_info(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/cookbook_info/cookbook1')
        assert response.status_code == 200
        expected_response = {
            'validity': True,
            'cookbook_name': 'Cookbook1',
            'online': False,
            'message': 'Physical book',
            'url': '',
            'recipes': ['recipe1', 'recipe2']
        }
        assert response.json == expected_response