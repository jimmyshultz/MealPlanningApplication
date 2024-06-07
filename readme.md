# Weekly Meal Planner

## Introduction

This is a web application for managing recipes and cookbooks. Users can add, view, and delete recipes and cookbooks. Each recipe includes a list of ingredients and each cookbook includes a list of recipes.

## Features

- Add, view, and delete recipes
- Add, view, and delete cookbooks
- Assign recipes to a day of the week for meal planning

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: MySQL

## Setup and Installation

1. Download and Install MySQL `https://dev.mysql.com/downloads/mysql/` or `brew install mysql` and `brew services start mysql`
2. Download and Install Python `https://www.python.org/downloads/`
3. Clone the repository: `git clone https://github.com/jimmyshultz/MealPlanningApplication`
4. Navigate to the project directory: `cd MealPlanningApplication`
5. Setup MealPlanningDatabase `mysql -u root - p < sql/CreateMealPlanning.sql`, `mysql -u root - p < sql/DatabaseUpdates.sql`, `mysql -u root - p < sql/AddingRemovingCookbooksRecipes.sql`
6. Install the dependencies: `pip install -r flask_app/requirements.txt`
7. Start the server: `python flask_app/backend/meal_planning_backend.py {your_db_username} {your_db_password}`

## Usage

1. Open index.html in the browser.
2. Click the cookbooks nav element to view cookbooks.
3. Click the recipes nav element to view recipes.
4. Add, delete, and view cookbooks, recipes, and ingredients as able through functionality.
5. Assign recipes to days of the week.