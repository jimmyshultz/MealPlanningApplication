"""
This file contains the CLI back-end of the meal planning application.\

It includes:
- Data Access Layer Class
- Business Logic Class
- An instance of the DAL to be used on the backend
- An instance of the Business Logic that uses the instance of the DAL 
  to be called on the frontend

The file is designed to by run through the frontend that imports it.
"""

import mysql.connector
import sys
import os
from mysql.connector import errorcode
from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

class DAL:
    """
    An object to interact with the MealPlanning SQL database providing 
    its data safely to the meal planning application
    
    Instantiation parameters:
    - database user name
    - database password

    Methods:
    - get cookbook names
    - get cookbook info
    - add cookbook
    - delete cookbook
    - update cookbook
    - get recipe names
    - get recipe info
    - get recipe ingredients
    - add recipe
    - delete recipe
    - update recipe
    - add ingredient
    - delete ingredient
    - update ingredient
    - add ingredient recipe pairing
    - add user
    - get user password
    - get user info
    """
    def __init__(self, p_user_name, p_dbpassword):
        self.dbuser_name = p_user_name
        self.dbpassword = p_dbpassword
        self.host = "127.0.0.1"
        self.database = "MealPlanning"

    def get_cookbook_names(self, user_id):
        """
        Retrieves the names of all cookbooks from the database.

        Returns:
            list: A list of cookbook names.
            str: An error message if there was an error connecting to the database.
        """
        cookbook_names = []
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            
            cursor = connector.cursor()
            cursor.callproc("GetAllCookbookNames", [user_id])
            for x in cursor.stored_results():
                for item in x.fetchall():
                    cookbook_names.append(item[0])
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Cannot connect to the database"
            else:
                return err
        
        else:
            connector.close()
            return cookbook_names
    
    def get_cookbook_info(self, cookbook_name, user_id):
        """
        Retrieves information about a cookbook from the database.

        Parameters:
        - cookbook_name (str): The name of the cookbook to retrieve information for.

        Returns:
        - tuple: A tuple containing the information about the cookbook, or None if the cookbook does not exist.

        Raises:
        - mysql.connector.Error: If there is an error accessing the database.
        """
        try:
            cookbook_info = ()
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            
            cursor = connector.cursor()
            cursor.callproc("GetCookbookInfo", [cookbook_name, user_id])
            for x in cursor.stored_results():
                cookbook_info = x.fetchone()
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return err
        
        else:
            connector.close()
            return cookbook_info
        
    def add_cookbook(self, cookbook_name, is_book, user_id, website=None):
        """
        Adds a new cookbook to the database.
    
        Parameters:
        - cookbook_name (str): The name of the cookbook to be added.
    
        Outputs:
        - str: A success message if the cookbook is added successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("AddCookbook", [cookbook_name, is_book, website, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for cookbook already existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Cookbook '{cookbook_name}' added successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
        
    def delete_cookbook(self, cookbook_name, user_id):
        """
        Deletes a cookbook from the database.
    
        Parameters:
        - cookbook_name (str): The name of the cookbook to be deleted.
    
        Outputs:
        - str: A success message if the cookbook is deleted successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("DeleteCookbook", [cookbook_name, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for cookbook not existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Cookbook '{cookbook_name}' deleted successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
        
    def update_cookbook(self, current_cookbook_name, new_cookbook_name, new_is_book, user_id, new_website=None):
        """
        Updates the name of a cookbook in the database.

        Parameters:
        - current_cookbook_name (str): The current name of the cookbook.
        - new_cookbook_name (str): The new name for the cookbook.
        - new_is_book (bool): Indicates whether the cookbook is a book or not.
        - new_website (str, optional): The new website for the cookbook. Defaults to None.

        Outputs:
        - str: A success message if the cookbook is updated successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("UpdateCookbook", [current_cookbook_name, 
                                            new_cookbook_name, new_is_book, 
                                            new_website, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for cookbook not existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Cookbook '{new_cookbook_name}' updated successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
        
    def get_recipe_names(self, user_id, cookbook_name=""):
        """
        Retrieves the names of all recipes from a specified cookbook.
    
        Parameters:
        - cookbook_name (str): The name of the cookbook from which to retrieve recipe names.
    
        Returns:
        - list: A list of recipe names if successful.
        - str: An error message if an error occurs.
        """
        recipe_names = []
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            
            cursor = connector.cursor()
            if cookbook_name == "":
                cursor.callproc("GetAllRecipeNames", [user_id])
                for x in cursor.stored_results():
                    for item in x.fetchall():
                        recipe_names.append(item[0])
            else:
                cursor.callproc("GetRecipesFromOneCookbook", [cookbook_name, user_id])
                for x in cursor.stored_results():
                    for item in x.fetchall():
                        recipe_names.append(item[0])
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return err
        
        else:
            connector.close()
            return recipe_names
    
    def get_recipe_info(self, recipe_name, user_id):
        """
        Retrieves information about a specific recipe.
    
        Parameters:
        - recipe_name (str): The name of the recipe for which to retrieve information.
    
        Returns:
        - tuple: A tuple containing recipe information if successful.
        - str: An error message if an error occurs.
        """
        try:
            recipe_info = ()
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            
            cursor = connector.cursor()
            cursor.callproc("GetRecipeInfo", [recipe_name, user_id])
            for x in cursor.stored_results():
                recipe_info = x.fetchone()
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return err
        
        else:
            connector.close()
            return recipe_info
        
    def get_recipe_ingredients(self, recipe_name, user_id):
        """
        Retrieves the ingredients of a specific recipe.
    
        Parameters:
        - recipe_name (str): The name of the recipe for which to retrieve ingredients.
    
        Returns:
        - list: A list of ingredients if successful.
        - str: An error message if an error occurs.
        """
        try:
            recipe_ingredients = []
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            
            cursor = connector.cursor()
            cursor.callproc("GetMealIngredients", [recipe_name, user_id])
            for x in cursor.stored_results():
                for item in x.fetchall():
                    recipe_ingredients.append(item[0])
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return err
        
        else:
            connector.close()
            return recipe_ingredients
        
    def add_recipe(self, recipe_name, cookbook_name, servings, user_id):
        """
        Adds a new recipe to the database.
    
        Parameters:
        - recipe_name (str): The name of the recipe to be added.
    
        Outputs:
        - str: A success message if the recipe is added successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("AddRecipe", [recipe_name, cookbook_name, servings, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for recipe already existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Recipe '{recipe_name}' added successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
    
    def delete_recipe(self, recipe_name, user_id):
        """
        Deletes a recipe from the database.
    
        Parameters:
        - recipe_name (str): The name of the recipe to be deleted.
    
        Outputs:
        - str: A success message if the recipe is deleted successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("DeleteRecipe", [recipe_name, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for recipe not existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Recipe '{recipe_name}' deleted successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
    
    def update_recipe(self, current_recipe_name, new_recipe_name, new_cookbook_name, new_servings, user_id):
        """
        Updates the name of a recipe in the database.

        Parameters:
        - current_recipe_name (str): The current name of the recipe.
        - new_recipe_name (str): The new name for the recipe.
        - new_cookbook_name (str): The new name of the cookbook the recipe belongs to.
        - new_servings (int): The new number of servings for the recipe.

        Outputs:
        - str: A success message if the recipe is updated successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("UpdateRecipe", [current_recipe_name, 
                                             new_recipe_name, 
                                             new_cookbook_name, new_servings, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for recipe not existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Recipe '{new_recipe_name}' updated successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
        
    def add_ingredient(self, ingredient_name, user_id):
        """
        Adds a new ingredient to the database.
    
        Parameters:
        - ingredient_name (str): The name of the ingredient to be added.
    
        Outputs:
        - str: A success message if the ingredient is added successfully.
        - str: An error message if an error occurs.
        """

        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("AddIngredient", [ingredient_name, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for ingredient already existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Ingredient '{ingredient_name}' added successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
        
    def delete_ingredient(self, ingredient_name, user_id):
        """
        Deletes an ingredient from the database.
    
        Parameters:
        - ingredient_name (str): The name of the ingredient to be deleted.
    
        Outputs:
        - str: A success message if the ingredient is deleted successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("DeleteIngredient", [ingredient_name, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for ingredient not existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Ingredient '{ingredient_name}' deleted successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")
        
    def update_ingredient(self, current_ingredient_name, new_ingredient_name, user_id):
        """
        Updates the name of an ingredient in the database.
    
        Parameters:
        - current_ingredient_name (str): The current name of the ingredient.
        - new_ingredient_name (str): The new name for the ingredient.
    
        Outputs:
        - Prints a success message to the console if the ingredient is updated successfully.
        - Prints an error message to the console if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("UpdateIngredient", [current_ingredient_name, 
                                                 new_ingredient_name, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':  # Custom SQLSTATE for ingredient not existing
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Ingredient '{new_ingredient_name}' updated successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")

    def add_ingredient_recipe_pairing(self, ingredient_name, recipe_name, user_id):
        """
        Adds a new ingredient-recipe pairing to the database.
    
        Parameters:
        - ingredient_name (str): The name of the ingredient to be paired.
        - recipe_name (str): The name of the recipe to be paired.
    
        Outputs:
        - str: A success message if the pairing is added successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("AddIngredientRecipePairing", [ingredient_name, 
                                                           recipe_name, user_id])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.sqlstate == '45000':
                print(f"Error: {err.msg}")
            else:
                print(err)
        else:
            connector.commit()
            print(f"Ingredient '{ingredient_name}' paired with recipe '{recipe_name}' successfully.")
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")

    def add_user(self, email, password, first_name, last_name):
        """
        Adds a new user to the database.
    
        Parameters:
        - email (str): The email of the new user.
        - password (str): The password of the new user.
        - first_name (str): The first name of the new user.
        - last_name (str): The last name of the new user.
    
        Outputs:
        - str: A success message if the user is added successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("AddUser", [email, password, first_name, last_name])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            elif err.sqlstate == '45000':
                return f"Error: {err.msg}"
            else:
                return err
        else:
            connector.commit()
            return f"User '{email}' added successfully."
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()
                print("MySQL connection is closed.")

    def delete_user(self, email):
        """
        Deletes a user from the database.

        Parameters:
        - email (str): The email of the user to delete.

        Outputs:
        - str: A success message if the user is deleted successfully.
        - str: An error message if an error occurs.
        """
        try:
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            cursor = connector.cursor()
            cursor.callproc("DeleteUser", [email])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            elif err.sqlstate == '45000':
                return f"Error: {err.msg}"
            else:
                return err
        else:
            connector.commit()
            return f"User '{email}' deleted successfully."
        finally:
            if cursor:
                cursor.close()
            if connector and connector.is_connected():
                connector.close()

    def get_user_password(self, email):
        """
        Retrieves the password of a user from the database.
    
        Parameters:
        - email (str): The email of the user whose password is to be retrieved.
    
        Returns:
        - str: The password of the user if successful.
        - str: An error message if an error occurs.
        """
        try:
            user_password = ""
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            
            cursor = connector.cursor()
            cursor.callproc("GetUserPassword", [email])
            for x in cursor.stored_results():
                user_password = x.fetchone()[0]
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return err
        
        else:
            connector.close()
            return user_password
        
    def get_user_info(self, email):
        """
        Retrieves information about a user from the database.
    
        Parameters:
        - email (str): The email of the user whose information is to be retrieved.
    
        Returns:
        - tuple: A tuple containing the information about the user if successful.
        - str: An error message if an error occurs.
        """
        try:
            user_info = ()
            connector = mysql.connector.connect(user=self.dbuser_name, 
                                                password=self.dbpassword,
                                                host=self.host,
                                                database=self.database)
            
            cursor = connector.cursor()
            cursor.callproc("GetUserInfo", [email])
            for x in cursor.stored_results():
                user_info = x.fetchone()
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return err
        
        else:
            connector.close()
            return user_info
        
class BusinessLogic:
    """
    An object to interface between the Data Access Layer (DAL) and the client, providing the necessary 
    information to the frontend while shielding the database from the user.

    Instantiation Parameters:
    - Data Access Layer object

    Methods:
    - register_routes: Registers all the routes for the Flask application.
        - check_recipe: Checks if a given recipe name is valid.
        - get_cookbook_names: Returns a list of all cookbook names in the database.
        - get_cookbook_info: Checks if a given cookbook name is in the active list and returns its information.
        - get_recipe_names: Returns a list of all recipe names in a specific cookbook.
        - get_all_recipe_names: Returns a list of all recipe names in the database.
        - get_recipe_info: Checks if a given recipe name is in the active list and returns its information.
        - add_cookbook: Adds a new cookbook to the database.
        - delete_cookbook: Deletes a cookbook from the database.
        - add_recipe: Adds a new recipe to the database.
        - delete_recipe: Deletes a recipe from the database.
        - add_ingredient: Adds a new ingredient to the database.
        - delete_ingredient: Deletes an ingredient from the database.
        - add_ingredient_recipe_pairing: Adds a new ingredient-recipe pairing to the database.
        - add_user: Adds a new user to the database.
        - login_user: Logs a user into the application.
    - run: Starts the Flask application.
    """
    def __init__(self, p_dal):
        self.dal = p_dal
        self.app = Flask(__name__)
        self.cors = CORS()
        self.register_routes()

    def register_routes(self):

        self.app.debug = True
        self.app.config.update(
            SESSION_COOKIE_SAMESITE='None', 
            SESSION_COOKIE_SECURE=True
        )
        self.cors.init_app(self.app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:8000"}})
        self.app.secret_key = os.environ.get('SECRET_KEY')
        
        @self.app.route('/check_recipe/<p_recipe>')
        def check_recipe(p_recipe):
            """
            This method checks if a user-given recipe name is valid.
        
            Parameters:
            - p_recipe (str): The recipe name to be checked.
        
            Returns:
            - JSON response: A dictionary with a 'validity' key. The value is 
              True if the recipe name is valid, False otherwise.
            """
            response_dict = { 'validity' : False }
            current_user_id = session.get('user_id')
            all_recipe_names = self.dal.get_recipe_names(user_id=current_user_id)
            if p_recipe in all_recipe_names:
                response_dict['validity'] = True
            else:
                response_dict['validity'] = False

            response = make_response(jsonify(response_dict))
            response.content_type = 'application/json'
            return response

        @self.app.route('/cookbook_names', methods=['GET', 'OPTIONS'])
        def get_cookbook_names():
            """
            This method returns a list of all the names of all the cookbooks in the database.
        
            Returns:
            - JSON response: A list of all cookbook names in the database.
            """
            
            current_user_id = session.get('user_id')
            print(current_user_id)
            all_cookbook_names = self.dal.get_cookbook_names(current_user_id)
            print(all_cookbook_names)
            response = make_response(jsonify(all_cookbook_names))
            response.content_type = 'application/json'
            print(response)
            return response
        
        @self.app.route("/cookbook_info/<p_cookbook>") 
        def get_cookbook_info(p_cookbook):
            """
            This method checks if a user-given cookbook name is in the active list of cookbook names.
            
            Parameters:
            - p_cookbook (str): The cookbook name to be checked.
        
            Returns:
            - JSON response: A dictionary with keys 'validity', 'message', and 'recipes'. 
              'validity' is True if the cookbook name is valid, False otherwise. 
              'message' contains information about the cookbook. 
              'recipes' is a list of recipes in the cookbook.
            """
            response_dict = { 'validity' : False, 'message': '', 'recipes': [] }
            current_user_id = session.get('user_id')
            current_cookbook_names = self.dal.get_cookbook_names(current_user_id)
            cookbook = p_cookbook
            if cookbook in current_cookbook_names:
                cookbook_info = self.dal.get_cookbook_info(cookbook, current_user_id)
                cookbook_recipes = self.dal.get_recipe_names(user_id=current_user_id, cookbook_name=cookbook)
                if cookbook_info[1] == 1:
                    response_dict["validity"] = True
                    response_dict["message"] = f"\n{cookbook_info[0]} is a book."
                    response_dict["recipes"] = cookbook_recipes
                else:
                    response_dict["validity"] = True
                    response_dict["message"] = f"\n{cookbook_info[0]} is viewable on the internet at {cookbook_info[2]}"
                    response_dict["recipes"] = cookbook_recipes
            else:
                response_dict["validity"] = False
                response_dict["message"] = ""

            response = make_response(jsonify(response_dict))
            response.content_type = 'application/json'
            return response
        
        @self.app.route('/add_cookbook', methods=['PUT'])
        def add_cookbook():
            """
            This method adds a new cookbook to the database.
        
            Parameters:
            - JSON request data with keys 'new_cookbook_name', 'new_is_book', and 'new_website'.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the success of the operation.
            - HTTP status code: 200 on success.
            """
            data = request.json
            cookbook_name = data['new_cookbook_name']
            is_book = data['new_is_book']
            website = data['new_website']

            #Call the DAL method to add the cookbook
            current_user_id = session.get('user_id')
            print(current_user_id)
            print(type(current_user_id))
            self.dal.add_cookbook(cookbook_name, is_book, current_user_id, website)
            response_dict = { 'message': f'Cookbook {cookbook_name} added successfully'}
            return jsonify(response_dict), 200
        
        @self.app.route("/delete_cookbook/<p_cookbook>", methods=['DELETE'])
        def delete_cookbook(p_cookbook):
            """
            This method deletes a cookbook from the database.
        
            Parameters:
            - p_cookbook (str): The name of the cookbook to be deleted.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the success of the operation.
            - HTTP status code: 200 on success.
            """
            current_user_id = session.get('user_id')
            self.dal.delete_cookbook(p_cookbook, current_user_id)
            response_dict = { 'message': f'Cookbook {p_cookbook} deleted successfully'}
            return jsonify(response_dict), 200


        @self.app.route("/recipe_names/<p_cookbook>")    
        def get_recipe_names(p_cookbook):
            """
            This method returns a list of all the names of the recipes of a 
            certain cookbook in the database.
        
            Parameters:
            - p_cookbook (str): The name of the cookbook.
        
            Returns:
            - JSON response: A list of all recipe names in the specified cookbook.
            """
            current_user_id = session.get('user_id')
            all_recipe_names = self.dal.get_recipe_names(user_id=current_user_id, cookbook_name=p_cookbook)
            response = make_response(jsonify(all_recipe_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route("/all_recipe_names")
        def get_all_recipe_names():
            """
            This method returns a list of the names of all the recipes in the database.
        
            Returns:
            - JSON response: A list of all recipe names in the database.
            """
            current_user_id = session.get('user_id')
            all_recipe_names = self.dal.get_recipe_names(user_id=current_user_id)
            response = make_response(jsonify(all_recipe_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route("/recipe_info/<p_recipe>")
        def get_recipe_info(p_recipe):
            """
            This method retrieves information about a given recipe.
        
            Parameters:
            - p_recipe (str): The name of the recipe to be checked.
        
            Returns:
            - JSON response: A dictionary with keys 'message' and 'ingredients'. 
              'message' contains information about the recipe. 
              'ingredients' is a list of ingredients for the recipe.
            """
            current_user_id = session.get('user_id')
            recipe_info = self.dal.get_recipe_info(p_recipe, current_user_id)
            recipe_ingredients = self.dal.get_recipe_ingredients(p_recipe, current_user_id)
            info_message = f"{recipe_info[0]} comes from {recipe_info[1]} and serves {recipe_info[2]} using: "

            response_dict = { 'message' : info_message, 'ingredients' : recipe_ingredients}
            response = make_response(jsonify(response_dict))
            response.content_type = 'application/json'
            return response
        
        @self.app.route('/add_recipe', methods=['PUT'])
        def add_recipe():
            """
            This method adds a new recipe to the database.
        
            Parameters:
            - JSON request data with keys 'new_recipe_name', 'new_cookbook_name', and 'new_servings'.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the success of the operation.
            - HTTP status code: 200 on success.
            """
            data = request.json
            recipe_name = data['new_recipe_name']
            cookbook_name = data['new_cookbook_name']
            servings = data['new_servings']

            #Call the DAL method to add the cookbook
            current_user_id = session.get('user_id')
            self.dal.add_recipe(recipe_name, cookbook_name, servings, current_user_id)
            response_dict = { 'message': f'Recipe {recipe_name} added successfully'}
            return jsonify(response_dict), 200

        @self.app.route("/delete_recipe/<p_recipe>", methods=['DELETE'])
        def delete_recipe(p_recipe):
            """
            This method deletes a recipe from the database.
        
            Parameters:
            - p_recipe (str): The name of the recipe to be deleted.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the success of the operation.
            - HTTP status code: 200 on success.
            """
            current_user_id = session.get('user_id')
            self.dal.delete_recipe(p_recipe, current_user_id)
            response_dict = { 'message': f'Recipe {p_recipe} deleted successfully'}
            return jsonify(response_dict), 200
        
        @self.app.route('/add_ingredient', methods=['PUT'])
        def add_ingredient():
            """
            This method adds a new ingredient to the database.
        
            Parameters:
            - JSON request data with a key 'ingredient_name'.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the success of the operation.
            - HTTP status code: 200 on success.
            """
            data = request.json
            ingredient_name = data['new_ingredient']

            #Call the DAL method to add the ingredient
            current_user_id = session.get('user_id')
            self.dal.add_ingredient(ingredient_name, current_user_id)
            response_dict = { 'message': f'Ingredient {ingredient_name} added successfully'}
            return jsonify(response_dict), 200
        
        @self.app.route("/delete_ingredient/<p_ingredient>", methods=['DELETE'])
        def delete_ingredient(p_ingredient):
            """
            This method deletes an ingredient from the database.
        
            Parameters:
            - p_ingredient (str): The name of the ingredient to be deleted.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the success of the operation.
            - HTTP status code: 200 on success.
            """
            current_user_id = session.get('user_id')
            self.dal.delete_ingredient(p_ingredient, current_user_id)
            response_dict = { 'message': f'Ingredient {p_ingredient} deleted successfully'}
            return jsonify(response_dict), 200
        
        @self.app.route('/add_ingredient_recipe_pairing', methods=['PUT'])
        def add_ingredient_recipe_pairing():
            """
            This method adds a new ingredient-recipe pairing to the database.
        
            Parameters:
            - JSON request data
                - 'ingredient_name': The name of the ingredient to be paired.
                - 'recipe_name': The name of the recipe to be paired.
            
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the success of the operation.
            - HTTP status code: 200 on success.
            """
            data = request.json
            ingredient_name = data['ingredient_name']
            recipe_name = data['recipe_name']

            #Call the DAL method to add the pairing
            current_user_id = session.get('user_id')
            self.dal.add_ingredient_recipe_pairing(ingredient_name, recipe_name, current_user_id)
            response_dict = { 'message': f'Ingredient {ingredient_name} paired with recipe {recipe_name} successfully'}
            return jsonify(response_dict), 200
        
        @self.app.route('/add_user', methods=['PUT'])
        def add_user():
            """
            This method adds a new user to the database.
        
            Parameters:
            - JSON request data with keys 'username', 'email', 'password', 
              'first_name', and 'last_name'.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the 
              success of the operation.
            - HTTP status code: 200 on success.
            """
            data = request.json
            email = data['email']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']

            #Hash the password
            hashed_password = generate_password_hash(password)

            #Call the DAL method to add the user
            result = self.dal.add_user(email, hashed_password, first_name, last_name)
            print(result)

            #Check the result and return the appropriate response
            if result == "Something is wrong with your user name or password" or result == "Database does not exist" or result == "Error: User already exists":
                response_dict = { 'message': f"Error: {result}", 'success': False}
                return jsonify(response_dict), 400
            else:
                response_dict = { 'message': f'User {email} added successfully', 'success': True}
                return jsonify(response_dict), 200
            
        @self.app.route('/delete_user', methods=['DELETE'])
        def delete_user():
            """
            This method deletes a user from the database.

            Parameters:
            - JSON request data with key 'email'.

            Returns:
            - JSON response: A dictionary with a 'message' key indicating the 
                success of the operation.
            - HTTP status code: 200 on success, 400 on failure.
            """
            data = request.json
            email = data['email']

            # Call the DAL method to delete the user
            result = self.dal.delete_user(email)
            print(result)

            # Check the result and return the appropriate response
            if result == "Something is wrong with your user name or password" or result == "Database does not exist" or result.startswith("Error:"):
                    response_dict = { 'message': f"Error: {result}", 'success': False}
                    return jsonify(response_dict), 400
            else:
                    response_dict = { 'message': f'User {email} deleted successfully', 'success': True}
                    return jsonify(response_dict), 200
            
        @self.app.route('/login', methods=['POST'])
        def login():
            """
            This method logs a user into the application.
        
            Parameters:
            - JSON request data with keys 'email' and 'password'.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the 
              success of the operation.
            - HTTP status code: 200 on success.
            """
            data = request.json
            email = data['email']
            password = data['password']

            # Get the hashed password from the database
            user_info = self.dal.get_user_info(email)
            print(user_info)
            # Need to fix this to check if a user exists before trying to take the pieces of information from user_info
            hashed_password = user_info[2]
        
            # Check if the password is correct
            if check_password_hash(hashed_password, password):
                # Store the user's id in the session
                session['user_id'] = user_info[0]
                print(session['user_id'])
        
                response_dict = {'message': f'User {email} logged in successfully', 
                                 'success': True,
                                 'first_name': user_info[3],
                                 'last_name': user_info[4],
                                 'email': user_info[1]}
                return jsonify(response_dict), 200
            else:
                response_dict = { 'message': 'Error: Incorrect password', 'success': False}
                return jsonify(response_dict), 400
            
        @self.app.route('/logout', methods=['POST'])
        def logout():
            """
            This method logs a user out of the application.
        
            Returns:
            - JSON response: A dictionary with a 'message' key indicating the 
              success of the operation.
            - HTTP status code: 200 on success.
            """
            # Remove the user's id from the session
            session.pop('user_id', None)
        
            response_dict = {'message': 'User logged out successfully', 'success': True}
            return jsonify(response_dict), 200
            
    def run(self):
        """
        This method starts the Flask application on the local machine.
    
        The application will be accessible at 'localhost' on port '50051'.
        """
        print("Listening at 'localhost:50051'...")
        self.app.run(host='0.0.0.0', port=50051)
    
if __name__ == '__main__':      
    my_dal = DAL(sys.argv[1], sys.argv[2])
    my_bl = BusinessLogic(my_dal)
    my_bl.run()
