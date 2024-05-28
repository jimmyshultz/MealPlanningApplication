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
    its data safely to the meal planning applicaiton
    
    Instantiation parameters:
    - database user name
    - database password

    Methods:
    - get cookbook names
    - get cookbook info
    - get recipe names
    - get recipe info
    - get recipe ingredients
    
    """
    def __init__(self, p_user_name, p_dbpassword):
        self.dbuser_name = p_user_name
        self.dbpassword = p_dbpassword
        self.host = "127.0.0.1"
        self.database = "MealPlanning"

    def get_cookbook_names(self):
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
                return "Database does not exist"
            else:
                return err
        
        else:
            connector.close()
            return cookbook_names
    
    def get_cookbook_info(self, cookbook_name):
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
        
    #add cookbook
    def add_cookbook(self, cookbook_name, is_book, website=None):
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
        
    #delete cookbook
    def delete_cookbook(self, cookbook_name):
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
        
    #update cookbook
    def update_cookbook(self, current_cookbook_name, new_cookbook_name, new_is_book, new_website=None):
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
        
    #add recipe
    def add_recipe(self, recipe_name, cookbook_name, servings):
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
    
    #delete recipe
    def delete_recipe(self, recipe_name):
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
    
    #update recipe
    def update_recipe(self, current_recipe_name, new_recipe_name, new_cookbook_name, new_servings):
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
        
    #add ingredient
    def add_ingredient(self, ingredient_name):
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
        
    #delete ingredient
    def delete_ingredient(self, ingredient_name):
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
        
    #update ingredient
    def update_ingredient(self, current_ingredient_name, new_ingredient_name):
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
    An object to interface between the DAL and the client providing the proper 
    information to the frontend while shielding the database further from the 
    user.

    Instantiation Parameters:
    - Data Access Layer object

    Methods:
    - check day
    - check recipe
    - get cookbook names
    - get cookbook info
    - get recipe names
    - get recipe info
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
            This method checks if user given recipe name is valid.
            
            Parameters:
            - string recipe name to be checked
    
            Returns:
            - True or False
    
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
            This method returns a list of all the names of all the 
            cookbooks in the database.
            """
            all_cookbook_names = self.dal.get_cookbook_names()
            response = make_response(jsonify(all_cookbook_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route("/cookbook_info/<p_cookbook>") 
        def get_cookbook_info(p_cookbook):
            """
            This method checks if user given cookbook name is in the active list of
             cookbook names.
            
            Parameters:
            - list of active cookbook names
            - string cookbook name to be checked
    
            Returns:
            - True or False
            - string message of information about the cookbook
    
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
            self.dal.delete_cookbook(p_cookbook)
            response_dict = { 'message': f'Cookbook {p_cookbook} deleted successfully'}
            return jsonify(response_dict), 200


        @self.app.route("/recipe_names/<p_cookbook>")    
        def get_recipe_names(p_cookbook):
            """
            This method returns a list of all the names of the 
            recipes of a certain cookbook in the database.
            """
            all_recipe_names = self.dal.get_recipe_names(p_cookbook)
            response = make_response(jsonify(all_recipe_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route("/all_recipe_names")
        def get_all_recipe_names():
            """
            This method returns a list of the names of 
            all the recipes in the database.
            """
            all_recipe_names = self.dal.get_recipe_names()
            response = make_response(jsonify(all_recipe_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route("/recipe_info/<p_recipe>")
        def get_recipe_info(p_recipe):
            """
            This method checks if user given recipe name is in the active list of
             recipe names.
            
            Parameters:
            - list of active recipe names
            - string recipe name to be checked
    
            Returns:
            - True or False
            - string message of information about the cookbook
            - list of recipe ingredients
    
            """
            recipe_info = self.dal.get_recipe_info(p_recipe)
            recipe_ingredients = self.dal.get_recipe_ingredients(p_recipe)
            info_message = f"{recipe_info[0]} comes from {recipe_info[1]} and serves {recipe_info[2]} using: "

            response_dict = { 'message' : info_message, 'ingredients' : recipe_ingredients}
            response = make_response(jsonify(response_dict))
            response.content_type = 'application/json'
            return response
        
        #add recipe
        @self.app.route('/add_recipe', methods=['PUT'])
        def add_recipe():
            data = request.json
            recipe_name = data['new_recipe_name']
            cookbook_name = data['new_cookbook_name']
            servings = data['new_servings']

            #Call the DAL method to add the cookbook
            self.dal.add_recipe(recipe_name, cookbook_name, servings)
            response_dict = { 'message': f'Recipe {recipe_name} added successfully'}
            return jsonify(response_dict), 200

        #delete recipe
        @self.app.route("/delete_recipe/<p_recipe>", methods=['DELETE'])
        def delete_recipe(p_recipe):
            self.dal.delete_recipe(p_recipe)
            response_dict = { 'message': f'Recipe {p_recipe} deleted successfully'}
            return jsonify(response_dict), 200
            
    def run(self):
        print("Listening at 'localhost:50051'...")
        self.app.run(host='localhost', port=50051)
    
if __name__ == '__main__':      
    my_dal = DAL(sys.argv[1], sys.argv[2])
    my_bl = BusinessLogic(my_dal)
    my_bl.run()
