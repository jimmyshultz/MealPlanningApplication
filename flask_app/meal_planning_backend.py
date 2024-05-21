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
from flask import Flask, jsonify, make_response

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
        self.register_routes()

    def register_routes(self):

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
        def get_cookbook_names():
            """
            This method returns a list of all the names of all the 
            cookbooks in the database.
            """
            all_cookbook_names = self.dal.get_cookbook_names()
            response = make_response(jsonify(all_cookbook_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route('/cookbook_info/<p_cookbook>') 
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
            response_dict = { 'validity' : False, 'message': '' }
            current_cookbook_names = self.dal.get_cookbook_names()
            cookbook = p_cookbook.title()
            if cookbook in current_cookbook_names:
                cookbook_info = self.dal.get_cookbook_info(cookbook)
                if cookbook_info[1] == 1:
                    response_dict["validity"] = True
                    response_dict["message"] = f"\n{cookbook_info[0]} is a book."
                else:
                    response_dict["validity"] = True
                    response_dict["message"] = f"\n{cookbook_info[0]} is viewable on the internet at {cookbook_info[2]}"
            else:
                response_dict["validity"] = False
                response_dict["message"] = ""

            response = make_response(jsonify(response_dict))
            response.content_type = 'application/json'
            return response

        @self.app.route('/recipe_names/<p_cookbook>')    
        def get_recipe_names(p_cookbook):
            """
            This method returns a list of all the names of the 
            recipes of a certain cookbook in the database.
            """
            all_recipe_names = self.dal.get_recipe_names(p_cookbook)
            response = make_response(jsonify(all_recipe_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route('/all_recipe_names')
        def get_all_recipe_names():
            """
            This method returns a list of the names of 
            all the recipes in the database.
            """
            all_recipe_names = self.dal.get_recipe_names()
            response = make_response(jsonify(all_recipe_names))
            response.content_type = 'application/json'
            return response
        
        @self.app.route('/recipe_info/<p_recipe>')
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
            
    def run(self):
        print("Listening at 'localhost:50051'...")
        self.app.run(host='localhost', port=50051)
    
if __name__ == '__main__':      
    my_dal = DAL(sys.argv[1], sys.argv[2])
    my_bl = BusinessLogic(my_dal)
    my_bl.run()