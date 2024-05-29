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
from mysql.connector import errorcode
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin

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
    """
    def __init__(self, p_user_name, p_dbpassword):
        self.dbuser_name = p_user_name
        self.dbpassword = p_dbpassword
        self.host = "127.0.0.1"
        self.database = "MealPlanning"

    def get_cookbook_names(self):
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
            cursor.callproc("GetAllCookbookNames")
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
    
    def get_cookbook_info(self, cookbook_name):
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
            cursor.callproc("GetCookbookInfo", [cookbook_name])
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
        
    def add_cookbook(self, cookbook_name, is_book, website=None):
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
            cursor.callproc("AddCookbook", [cookbook_name, is_book, website])
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
        
    def delete_cookbook(self, cookbook_name):
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
            cursor.callproc("DeleteCookbook", [cookbook_name])
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
        
    def update_cookbook(self, current_cookbook_name, new_cookbook_name, new_is_book, new_website=None):
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
                                            new_website])
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
        
    def get_recipe_names(self, cookbook_name=""):
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
                cursor.callproc("GetAllRecipeNames")
                for x in cursor.stored_results():
                    for item in x.fetchall():
                        recipe_names.append(item[0])
            else:
                cursor.callproc("GetRecipesFromOneCookbook", [cookbook_name])
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
    
    def get_recipe_info(self, recipe_name):
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
            cursor.callproc("GetRecipeInfo", [recipe_name])
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
        
    def get_recipe_ingredients(self, recipe_name):
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
            cursor.callproc("GetMealIngredients", [recipe_name])
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
        
    def add_recipe(self, recipe_name, cookbook_name, servings):
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
            cursor.callproc("AddRecipe", [recipe_name, cookbook_name, servings])
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
    
    def delete_recipe(self, recipe_name):
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
            cursor.callproc("DeleteRecipe", [recipe_name])
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
    
    def update_recipe(self, current_recipe_name, new_recipe_name, new_cookbook_name, new_servings):
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
                                             new_cookbook_name, new_servings])
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
        
    def add_ingredient(self, ingredient_name):
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
            cursor.callproc("AddIngredient", [ingredient_name])
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
        
    def delete_ingredient(self, ingredient_name):
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
            cursor.callproc("DeleteIngredient", [ingredient_name])
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
        
    def update_ingredient(self, current_ingredient_name, new_ingredient_name):
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
                                                 new_ingredient_name])
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
    - run: Starts the Flask application.
    """
    def __init__(self, p_dal):
        self.dal = p_dal
        self.app = Flask(__name__)
        self.cors = CORS()
        self.register_routes()

    def register_routes(self):

        self.app.debug = True
        self.cors.init_app(self.app)

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
            all_recipe_names = self.dal.get_recipe_names()
            if p_recipe in all_recipe_names:
                response_dict['validity'] = True
            else:
                response_dict['validity'] = False

            response = make_response(jsonify(response_dict))
            response.content_type = 'application/json'
            return response

        @self.app.route('/cookbook_names')
        @cross_origin()    
        def get_cookbook_names():
            """
            This method returns a list of all the names of all the cookbooks in the database.
        
            Returns:
            - JSON response: A list of all cookbook names in the database.
            """
            all_cookbook_names = self.dal.get_cookbook_names()
            response = make_response(jsonify(all_cookbook_names))
            response.content_type = 'application/json'
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
            current_cookbook_names = self.dal.get_cookbook_names()
            cookbook = p_cookbook.title()
            if cookbook in current_cookbook_names:
                cookbook_info = self.dal.get_cookbook_info(cookbook)
                cookbook_recipes = self.dal.get_recipe_names(cookbook)
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
            self.dal.add_cookbook(cookbook_name, is_book, website)
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
            self.dal.delete_cookbook(p_cookbook)
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
            all_recipe_names = self.dal.get_recipe_names(p_cookbook)
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
            all_recipe_names = self.dal.get_recipe_names()
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
            recipe_info = self.dal.get_recipe_info(p_recipe)
            recipe_ingredients = self.dal.get_recipe_ingredients(p_recipe)
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
            self.dal.add_recipe(recipe_name, cookbook_name, servings)
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
            self.dal.delete_recipe(p_recipe)
            response_dict = { 'message': f'Recipe {p_recipe} deleted successfully'}
            return jsonify(response_dict), 200
            
    def run(self):
        """
        This method starts the Flask application on the local machine.
    
        The application will be accessible at 'localhost' on port '50051'.
        """
        print("Listening at 'localhost:50051'...")
        self.app.run(host='localhost', port=50051)
    
if __name__ == '__main__':      
    my_dal = DAL(sys.argv[1], sys.argv[2])
    my_bl = BusinessLogic(my_dal)
    my_bl.run()
