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

    def check_day(self, p_day):
        """
        This method checks if user given day is valid.
        
        Parameters:
        - string day name to be checked

        Returns:
        - True or False
        - given day name properly formatted

        """
        days_of_week = ["monday", "tuesday", "wednesday", "thursday", 
                    "friday", "saturday", "sunday"]
        day = p_day.lower()
        day = day.strip()
        if day in days_of_week:
            return True, day
        else: 
            return False, day
        
    def check_recipe(self, p_recipe):
        """
        This method checks if user given recipe name is valid.
        
        Parameters:
        - string recipe name to be checked

        Returns:
        - True or False
        - given recipe name properly formatted

        """
        all_recipe_names = self.dal.get_recipe_names()
        recipe = p_recipe.title()
        if recipe in all_recipe_names:
            return True, recipe
        else:
            return False, recipe
        
    def get_cookbook_names(self):
        """
        This method returns a list of all the names of all the 
        cookbooks in the database.
        """
        all_cookbook_names = self.dal.get_cookbook_names()
        return all_cookbook_names
    
    def get_cookbook_info(self, current_cookbook_names, p_cookbook):
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
        cookbook = p_cookbook.title()
        if cookbook in current_cookbook_names:
            cookbook_info = self.dal.get_cookbook_info(cookbook)
            if cookbook_info[1] == 1:
                return True, f"\n{cookbook_info[0]} is a book."
            else:
                return True, f"\n{cookbook_info[0]} is viewable on the internet at {cookbook_info[2]}"
        else:
            return False, " "
        
    def get_recipe_names(self, p_cookbook):
        """
        This method returns a list of all the names of all the 
        recipes in the database.
        """
        all_recipe_names = self.dal.get_recipe_names(p_cookbook)
        return all_recipe_names
    
    def get_recipe_info(self, current_recipe_names, p_recipe):
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
        recipe = p_recipe.title()
        if recipe in current_recipe_names:
            recipe_info = self.dal.get_recipe_info(recipe)
            recipe_ingredients = self.dal.get_recipe_ingredients(recipe)
            info_message = f"{recipe_info[0]} comes from {recipe_info[1]} and serves {recipe_info[2]} using: "
            return True, info_message, recipe_ingredients
        else:
            return False, " ", []
        

my_dal = DAL(sys.argv[1], sys.argv[2])
my_bl = BusinessLogic(my_dal)