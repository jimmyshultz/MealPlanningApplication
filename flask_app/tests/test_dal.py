import pytest, os, sys

# Add the backend directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from meal_planning_backend import DAL, BusinessLogic

db_user_name = os.getenv('DB_USER_NAME')
db_password = os.getenv('DB_PASSWORD')

@pytest.fixture
def dal():
    return DAL(db_user_name, db_password)

class TestDAL:
    """
    A class to test the DAL class methods.

    Some tests use the test data that is included in the database 
    creation scripts.
    
    Tested Methods:
    - get cookbook names - test
    - get cookbook info - test
    - add cookbook - test
    - delete cookbook - test
    - get recipe names - test
    - get recipe info - test
    - get recipe ingredients - test
    - add recipe - test
    - delete recipe - test
    - add ingredient recipe pairing - test
    - add user - test
    - delete user - test
    - get user password - test
    - get user info - test

    Untested Methods:
    - update cookbook - not implemented
    - update recipe - not implemented
    - add ingredient - no return or get method to test
    - delete ingredient - no return or get method to test
    - update ingredient - not implemented
    """

    #Cookbook tests
    # Test DAL get cookbook names method
    def test_get_cookbook_names(self, dal):
    
        # Call the method to test
        cookbook_names = dal.get_cookbook_names(1)
    
        # Check that the method returned the correct cookbook names
        assert cookbook_names == ['Dinner Staples', 'Easy Meals', 'Half Baked Harvest - Brunch', 'Half Baked Harvest - Mains']
    
    # Test DAL get cookbook info method
    def test_get_cookbook_info(self, dal):
    
        # Call the method to test
        cookbook_info = dal.get_cookbook_info('Dinner Staples', 1)
    
        # Check that the method returned the correct cookbook information
        assert cookbook_info == ('Dinner Staples', 1, None, 1)

    # Test DAL add cookbook method
    def test_add_cookbook(self, dal):
    
        # Test data
        cookbook_name = 'Test Cookbook'
        user_id = 1
        is_book = True
        website = None
    
        # Delete the cookbook if it already exists
        dal.delete_cookbook(cookbook_name, user_id)
    
        # Call the method to test
        dal.add_cookbook(cookbook_name, is_book, user_id, website)
    
        # Retrieve the cookbook from the database to verify it was added correctly
        cookbook_info = dal.get_cookbook_info(cookbook_name, user_id)
    
        # Check that the retrieved cookbook's information matches the test data
        assert cookbook_info == (cookbook_name, 1, None, user_id)
    
        # Delete the cookbook
        dal.delete_cookbook(cookbook_name, user_id)

    # Test DAL delete cookbook method
    def test_delete_cookbook(self, dal):
    
        # Test data
        cookbook_name = 'Test Cookbook'
        user_id = 1
        is_book = True
        website = None
    
        # Add the cookbook to the database
        dal.add_cookbook(cookbook_name, is_book, user_id, website)
    
        # Call the method to test
        dal.delete_cookbook(cookbook_name, user_id)
    
        # Retrieve the cookbook from the database to verify it was deleted
        cookbook_info = dal.get_cookbook_info(cookbook_name, user_id)
    
        # Check that the cookbook does not exist in the database
        assert cookbook_info is None
    


    #Recipe tests
        
    # Test DAL get recipe names method
    def test_get_recipe_names(self, dal):
    
        # Call the method to test
        recipe_names = dal.get_recipe_names(1)
    
        # Check that the method returned the correct recipe names
        assert recipe_names == ['Beans & Rice', 'Blueberry Croissant French Toast Bake', 'Grilled Buffalo Ranch Chicken Tacos', 'Hamburgers', 'Macaroni & Cheese']
    
    # Test DAL get recipe info method
    def test_get_recipe_info(self, dal):
    
        # Call the method to test
        recipe_info = dal.get_recipe_info('Beans & Rice', 1)
    
        # Check that the method returned the correct recipe information
        assert recipe_info == ('Beans & Rice', 'Easy Meals', 2, 0, None, 1)

    # Test DAL get recipe ingredients method
    def test_get_recipe_ingredients(self, dal):
    
        # Call the method to test
        recipe_ingredients = dal.get_recipe_ingredients('Beans & Rice', 1)
    
        # Check that the method returned the correct recipe ingredients
        assert recipe_ingredients == ['Black Beans', 'White Rice']

    # Test DAL add recipe method
    def test_add_recipe(self, dal):
    
        # Test data
        recipe_name = 'Test Recipe'
        cookbook_name = 'Test Cookbook'
        user_id = 1
        servings = 2
        is_online = False
        webpage_link = None
    
        # Delete the recipe if it already exists
        dal.delete_recipe(recipe_name, user_id)

        # Delete the cookbook if it already exists
        dal.delete_cookbook(cookbook_name, user_id)

        # Add the cookbook to the database
        dal.add_cookbook(cookbook_name, True, user_id, None)
    
        # Call the method to test
        dal.add_recipe(recipe_name, cookbook_name, servings, is_online, user_id, webpage_link)
    
        # Retrieve the recipe from the database to verify it was added correctly
        recipe_info = dal.get_recipe_info(recipe_name, user_id)
    
        # Check that the retrieved recipe's information matches the test data
        assert recipe_info == (recipe_name, cookbook_name, servings, is_online, webpage_link, user_id)
    
        # Delete the cookbook
        dal.delete_cookbook(cookbook_name, user_id)

        # Delete the recipe
        dal.delete_recipe(recipe_name, user_id)
    
    # Test DAL delete recipe method
    def test_delete_recipe(self, dal):
    
        # Test data
        recipe_name = 'Test Recipe'
        cookbook_name = 'Test Cookbook'
        user_id = 1
        servings = 2
        is_online = False
        webpage_link = None
    
        # Add the cookbook to the database
        dal.add_cookbook(cookbook_name, True, user_id, None)

        # Add the recipe to the database
        dal.add_recipe(recipe_name, cookbook_name, servings, is_online, user_id, webpage_link)
    
        # Call the method to test
        dal.delete_recipe(recipe_name, user_id)
    
        # Retrieve the recipe from the database to verify it was deleted
        recipe_info = dal.get_recipe_info(recipe_name, user_id)
    
        # Check that the recipe does not exist in the database
        assert recipe_info is None
    
        # Delete the cookbook
        dal.delete_cookbook(cookbook_name, user_id)
    
    
    #Ingredient tests
        
    # Test DAL add ingredient recipe pairing method
    def test_add_ingredient_recipe_pairing(self, dal):
    
        # Test data
        cookbook_name = 'Test Cookbook'
        recipe_name = 'Test Recipe'
        ingredient_name = 'Test Ingredient'
        user_id = 1
    
        # Add the cookbook, recipe, and ingredient to the database
        dal.add_cookbook(cookbook_name, True, user_id, None)
        dal.add_recipe(recipe_name, cookbook_name, 2, False, user_id, None)
        dal.add_ingredient(ingredient_name, user_id)
    
        # Call the method to test
        dal.add_ingredient_recipe_pairing(ingredient_name, recipe_name, user_id)
    
        # Retrieve the ingredient recipe pairing from the database to verify it was added correctly
        test_recipe_ingredients = dal.get_recipe_ingredients(recipe_name, user_id)
    
        # Check that the retrieved ingredient recipe pairing matches the test data
        assert test_recipe_ingredients == [ingredient_name]
    
        # Delete the cookbooke, recipe, and ingredient
        dal.delete_cookbook(cookbook_name, user_id)
        dal.delete_recipe(recipe_name, user_id)
        dal.delete_ingredient(ingredient_name, user_id)
    
    #User tests
    #Test DAL add user method
    def test_add_user(self, dal):
    
        # Test data
        email = 'testuser@email.com'
        password = 'testpassword'
        first_name = 'Test'
        last_name = 'User'
    
        # Delete the user if it already exists
        dal.delete_user(email)
    
        # Call the method to test
        result = dal.add_user(email, password, first_name, last_name)
    
        # Check that the method returned a success message
        assert result == f"User '{email}' added successfully."
    
        # Retrieve the user from the database to verify it was added correctly
        user_info = dal.get_user_info(email)
        print(user_info)
    
        # Check that the retrieved user's information matches the test data
        assert isinstance(user_info[0], int) and user_info[0] > 0 and user_info[1:5] == (email, password, first_name, last_name)
    
        # Delete the user
        dal.delete_user(email)
    
    # Test DAL delete user method
    def test_delete_user(self, dal):
    
        # Test data
        email = 'testuser@example.com'
        password = 'testpassword'
        first_name = 'Test'
        last_name = 'User'
    
        # Add the user to the database
        dal.add_user(email, password, first_name, last_name)
    
        # Call the method to test
        result = dal.delete_user(email)
    
        # Check that the method returned a success message
        assert result == f"User '{email}' deleted successfully."
    
        # Retrieve the user from the database to verify it was deleted
        user_info = dal.get_user_info(email)
    
        # Check that the user does not exist in the database
        assert user_info == 'Error: User does not exist'
    
    # Test DAL get user password method
    def test_get_user_password(self, dal):
    
        # Test data
        email = 'testuser@example.com'
        password = 'testpassword'
        first_name = 'Test'
        last_name = 'User'
    
        # Add the user to the database
        dal.add_user(email, password, first_name, last_name)
    
        # Call the method to test
        result = dal.get_user_password(email)
    
        # Check that the method returned the correct password
        assert result == password
    
        # Delete the user
        dal.delete_user(email)
    
    # Test DAL get user info method
    def test_get_user_info(self, dal):
    
        # Test data
        email = 'testuser@example.com'
        password = 'testpassword'
        first_name = 'Test'
        last_name = 'User'
    
        # Add the user to the database
        dal.add_user(email, password, first_name, last_name)
    
        # Call the method to test
        user_info = dal.get_user_info(email)
    
        # Check that the method returned the correct user information
        assert isinstance(user_info[0], int) and user_info[0] > 0 and user_info[1:5] == (email, password, first_name, last_name)
    
        # Delete the user
        dal.delete_user(email)