"""
This file contains the CLI front-end of the meal planning application.

It includes:
- Class to store a client-side weekly meal plan
- A menu of operations
- A main function to execute the user's choice

For the application to work you should use MySQLWorkbench to create a MySQL 
database called MealPlanning using CreateMealPlanning.sql.  Then you'll need to 
run DatabaseUpdates.sql on MealPlanning to get the necessary stored procedures 
and functions.

This database was created in conjunction with the course CSC6302 at Merrimack 
College in Spring 2024 taught by Professor Rob Sand.  The application, however,
was entirely my work in a project.

To run the application in the terminal fill in your database user name and 
password and run `python meal_planning_terminal_application.py 
your_database_user_name your_database_password` in a directory that also 
contains meal_planning_backend.
"""
import meal_planning_backend

class WeeklyMealPlan:
    """An object to represent the client user's current week."""

    def __init__(self):
        self.monday = ""
        self.tuesday = ""
        self.wednesday = ""
        self.thursday = ""
        self.friday = ""
        self.saturday = ""
        self.sunday = ""

    def set_monday(self, recipe):
        self.monday = recipe

    def set_tuesday(self, recipe):
        self.tuesday = recipe

    def set_wednesday(self, recipe):
        self.wednesday = recipe

    def set_thursday(self, recipe):
        self.thursday = recipe

    def set_friday(self, recipe):
        self.friday = recipe

    def set_saturday(self, recipe):
        self.saturday = recipe

    def set_sunday(self, recipe):
        self.sunday = recipe

    def get_monday(self):
        return self.monday
    
    def get_tuesday(self):
        return self.tuesday
    
    def get_wednesday(self):
        return self.wednesday
    
    def get_thursday(self):
        return self.thursday
    
    def get_friday(self):
        return self.friday
    
    def get_saturday(self):
        return self.saturday
    
    def get_sunday(self):
        return self.sunday

def menu():
    """Display available operations to the user."""
    print("Enter 'w' to view the current week's plan "
          "\n'c' to view information about a cookbook "
          "\n'r' to view information about a recipe "
          "\n'a' to assign a recipe to a day of the week "
          "\n'q' to quit.")
    
def execute_user_action(weekly_meal_plan):
    """Interact with the backend to get database information to view or 
    properly update the client side weekly meal plan."""

    while True:
        print(" ")
        menu()
        action = input("\nWhat would you like to do? ")
    
        if action == 'q':
            print("Quitting.")
            break
    
        elif action == 'a':
            while True:
                day = input("What day of the week would you like to update? ")
                if day == 'q':
                    print("Quitting action.")
                    break
                day_validity, day = meal_planning_backend.my_bl.check_day(day)
                if day_validity == True:
                    break
                else:
                    print("Please enter a valid day of the week or 'q' to quit.")
    
            while True and day != 'q':
                recipe = input(f"What recipe would you like to eat on {day.title()}? ")
                if recipe == 'q':
                    print("Quitting action.")
                    break
                recipe_validity, recipe = meal_planning_backend.my_bl.check_recipe(recipe)
                if recipe_validity == True:
                    if day == "monday":
                        weekly_meal_plan.set_monday(recipe)
                    elif day == "tuesday":
                        weekly_meal_plan.set_tuesday(recipe)
                    elif day == "wednesday":
                        weekly_meal_plan.set_wednesday(recipe)
                    elif day == "thursday":
                        weekly_meal_plan.set_thursday(recipe)
                    elif day == "friday":
                        weekly_meal_plan.set_friday(recipe)
                    elif day == "saturday":
                        weekly_meal_plan.set_saturday(recipe)
                    elif day == "sunday":
                        weekly_meal_plan.set_sunday(recipe)
                    break
                else:
                    print("Please enter a valid recipe name or 'q' to quit.")
    
        elif action == "w":
            print(f"\nYour current weekly plan is: "
              f"\nMonday: {weekly_meal_plan.get_monday()} "
              f"\nTuesday: {weekly_meal_plan.get_tuesday()} "
              f"\nWednesday: {weekly_meal_plan.get_wednesday()} "
              f"\nThursday: {weekly_meal_plan.get_thursday()} "
              f"\nFriday: {weekly_meal_plan.get_friday()} "
              f"\nSaturday: {weekly_meal_plan.get_saturday()} "
              f"\nSunday: {weekly_meal_plan.get_sunday()} ")
            
        elif action == 'c':
            print("\nThe following cookbooks are currently in your database: ")
            my_cookbook_names = meal_planning_backend.my_bl.get_cookbook_names()
            for x in my_cookbook_names:
                print(x)
            while True:
                cookbook = input("\nWhich cookbook would you like to learn more about? ")
                if cookbook == 'q':
                    print("\nQuitting action.")
                    break
                cookbook_validity, info_message = meal_planning_backend.my_bl.get_cookbook_info(my_cookbook_names, cookbook)
                if cookbook_validity:
                    print(info_message)
                    break
                else:
                    print("\nPlease enter a valid cookbook name or 'q' to quit.")
        
        elif action == 'r':
            given_cookbook_name = input("\nPress enter if you'd like to see all "
                                        "recipes in the database or type in the"
                                        " name of any stored cookbook to view "
                                        "just its recipes: ")
            my_recipe_names = meal_planning_backend.my_bl.get_recipe_names(given_cookbook_name)
            for x in my_recipe_names:
                print(x)
            while True:
                recipe = input("\nWhich recipe would you like to learn more about? ")
                if recipe == 'q':
                    print("Quitting action.")
                    break
                recipe_validity, info_message, ingredient_list = meal_planning_backend.my_bl.get_recipe_info(my_recipe_names, recipe)
                if recipe_validity:
                    print(info_message)
                    for x in ingredient_list:
                        print(x)
                    break
                else:
                    print("Please enter a valid recipe name or 'q' to quit.")
            
            
        else:
            print("\nThat command is unrecognizable.  Enter 'q' to quit.")

if __name__ == '__main__':
    my_week = WeeklyMealPlan()
    execute_user_action(my_week)