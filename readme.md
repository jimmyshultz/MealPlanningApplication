# Weekly Meal Planner

## Introduction

This is a web application for managing recipes and cookbooks. Users can create accounts on which they can add, view, and delete recipes and cookbooks. Each recipe includes a list of ingredients and each cookbook includes a list of recipes.

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
7. Set the secret key, database username, and database password: `export SECRET_KEY={your_secret_key}`, `export DB_USER={your_db_username}`, `export DB_PASSWORD={your_db_password}`
8. Start the backend server: `python flask_app/backend/meal_planning_backend.py`
9. Open a second terminal and navigate to the frontend directory: `cd MealPlanningApplication/flask_app/web_based_frontend`
10. Start the frontend server: `python -m http.server 8000`

## Usage

1. Open http://localhost:8000/index.html in a Google Chrome or Mozilla Firefox browser.
2. Register an account through the register button.
3. Login into that account using the login button.
4. Click the cookbooks and recipes nav elements.
5. Add, delete, and view cookbooks, recipes, and ingredients as able through functionality.
6. Assign recipes to days of the week.

## Testing
1. Navigate to the tests directory: `cd tests`
2. Set the database username and password environment variables: `export DB_USER_NAME={your_db_user_name}, export DB_PASSWORD={your_db_password}`
3. Run DAL tests: `pytest test_dal.py`
4. Run BL tests: `pytest test_bl.py`