
"""
    A class to test the BusinessLogic class methods.

    Fixtures
    ----------
    - dal_mock - Mocks the Data Access Layer
    - app - Creates the Flask app with a mocked DAL
    - setup (in TestBL class) - Setup for each test method
    
    Tested Methods
    --------------
    - check_recipe
    - get_cookbook_names
    - get_cookbook_info
    - get_all_recipe_names
    - get_recipe_info
    - add_cookbook
    - delete_cookbook
    - add_recipe
    - delete_recipe
    - add_ingredient
    - delete_ingredient
    - add_ingredient_recipe_pairing
    - add_user
    - login_user
    
    Untested Methods
    ----------------
    - get_recipe_names - need to tie recipes to a cookbook in mock data
    
"""

import pytest, sys, os
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash

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
    mock.get_recipe_info.return_value = ('Recipe1', 'Cookbook1', 2, 1, 'http://example.com', 1)
    mock.get_recipe_ingredients.return_value = ['ingredient1', 'ingredient2']
    mock.get_user_info.return_value = (1, 'test@example.com', generate_password_hash('test'), 'test', 'test')
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

    def test_get_cookbook_info_invalid(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/cookbook_info/invalid_cookbook')
        assert response.status_code == 200
        assert response.json == { 'validity' : False, 'cookbook_name': '', 'online': False, 'message': '', 'url': '', 'recipes': [] }
    
    def test_get_all_recipe_names(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/all_recipe_names')
        assert response.status_code == 200
        assert response.json == ['recipe1', 'recipe2']

    def test_get_recipe_info(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/recipe_info/recipe1')
        assert response.status_code == 200
        expected_response = {
            'recipe_name': 'Recipe1',
            'cookbook_name': 'Cookbook1',
            'servings': 2,
            'is_online': 1,
            'url': 'http://example.com',
            'ingredients': ['ingredient1', 'ingredient2']
        }
        assert response.json == expected_response

    def test_add_cookbook(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.put('/add_cookbook', json={'new_cookbook_name': 'NewCookbook', 'new_website': 'http://example.com/', 'new_is_book': True})
        assert response.status_code == 200
        assert response.json == {'message': f'Cookbook NewCookbook added successfully'}

    def test_delete_cookbook(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.delete('/delete_cookbook/NewCookbook')
        assert response.status_code == 200
        assert response.json == {'message': f'Cookbook NewCookbook deleted successfully'}

    def test_add_recipe(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.put('/add_recipe', json={'new_recipe_name': 'NewRecipe', 'new_cookbook_name': 'Cookbook1', 'new_servings': 2, 'new_is_online': 1, 'new_webpage': 'http://example.com'})
        assert response.status_code == 200
        assert response.json == {'message': f'Recipe NewRecipe added successfully'}

    def test_delete_recipe(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.delete('/delete_recipe/NewRecipe')
        assert response.status_code == 200
        assert response.json == {'message': f'Recipe NewRecipe deleted successfully'}
    
    def test_add_ingredient(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.put('/add_ingredient', json={'new_ingredient': 'NewIngredient'})
        assert response.status_code == 200
        assert response.json == {'message': f'Ingredient NewIngredient added successfully'}

    def test_delete_ingredient(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.delete('/delete_ingredient/NewIngredient')
        assert response.status_code == 200
        assert response.json == {'message': f'Ingredient NewIngredient deleted successfully'}

    def test_add_ingredient_recipe_pairing(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.put('/add_ingredient_recipe_pairing', json={'recipe_name': 'Recipe1', 'ingredient_name': 'ingredient1'})
        assert response.status_code == 200
        assert response.json == {'message': f'Ingredient ingredient1 paired with recipe Recipe1 successfully'}

    def test_add_user(self):
        response = self.app.put('/add_user', json={'email': 'test@example.com', 'password': 'test', 'first_name': 'test', 'last_name': 'test'})
        assert response.status_code == 200
        assert response.json == {'message': f'User test@example.com added successfully', 'success': True}
    
    def test_login_user(self):
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'test'})
        assert response.json == {'message': f'User test@example.com logged in successfully', 'email': 'test@example.com', 'first_name': 'test', 'last_name': 'test', 'success': True}
        assert response.status_code == 200

    