DROP DATABASE IF EXISTS MealPlanning;

CREATE DATABASE MealPlanning;

USE  MealPlanning;

CREATE TABLE IF NOT EXISTS Cookbook (
CookbookName varchar(200)  not null,
IsBook bool not null,
Website varchar(200),
PRIMARY KEY ( CookbookName)
);

CREATE TABLE IF NOT EXISTS Recipe (
RecipeName varchar(100) not null,
CookbookName varchar (200) not null,
TotalServings int,
PRIMARY KEY (RecipeName),
FOREIGN KEY (CookbookName) REFERENCES Cookbook (CookbookName) on update cascade on delete cascade
);

CREATE TABLE IF NOT EXISTS Ingredients (
Id int not null auto_increment,
IngredientName varchar(100) not null,
PRIMARY KEY (Id)
);

CREATE TABLE IF NOT EXISTS Meal (
RecipeName varchar(100) not null,
IngredientId int not null,
PRIMARY KEY (RecipeName, IngredientId),
FOREIGN KEY (RecipeName) REFERENCES Recipe (RecipeName) on update cascade on delete cascade,
FOREIGN KEY (IngredientId) REFERENCES Ingredients (Id) on update cascade on delete cascade
);

-- Preliminary data

INSERT INTO Cookbook (CookbookName, IsBook) VALUES ("Easy Meals", true);
INSERT INTO Cookbook (CookbookName, IsBook) VALUES ("Dinner Staples", true);
INSERT INTO Cookbook (CookbookName, IsBook, Website) VALUES ("Half Baked Harvest - Mains", false, "https://www.halfbakedharvest.com/category/recipes/type-of-meal/main-course/");
INSERT INTO Cookbook (CookbookName, IsBook, Website) VALUES ("Half Baked Harvest - Brunch", false, "https://www.halfbakedharvest.com/category/recipes/type-of-meal/brunch/");

INSERT INTO Recipe (RecipeName, CookbookName, TotalServings) VALUES ("Macaroni & Cheese", "Easy Meals", 2);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings) VALUES ("Beans & Rice", "Easy Meals", 2);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings) VALUES ("Hamburgers", "Dinner Staples", 4);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings) VALUES ("Grilled Buffalo Ranch Chicken Tacos", "Half Baked Harvest - Mains", 6);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings) VALUES ("Blueberry Croissant French Toast Bake", "Half Baked Harvest - Brunch", 6);

-- Macaroni and Cheese

INSERT INTO Ingredients (IngredientName) VALUES ("Macaroni");
INSERT INTO Ingredients (IngredientName) VALUES ("Butter");
INSERT INTO Ingredients (IngredientName) VALUES ("Milk");
INSERT INTO Ingredients (IngredientName) VALUES ("Cheese Powder");

-- Beans and Rice

INSERT INTO Ingredients (IngredientName) VALUES ("Black Beans");
INSERT INTO Ingredients (IngredientName) VALUES ("White Rice");

-- Hamburgers

INSERT INTO Ingredients (IngredientName) VALUES ("Beef Patties");
INSERT INTO Ingredients (IngredientName) VALUES ("Tomato");
INSERT INTO Ingredients (IngredientName) VALUES ("Lettuce");
INSERT INTO Ingredients (IngredientName) VALUES ("Hamburger Buns");
INSERT INTO Ingredients (IngredientName) VALUES ("Ketchup");
INSERT INTO Ingredients (IngredientName) VALUES ("Mustard");
INSERT INTO Ingredients (IngredientName) VALUES ("Pickles");
INSERT INTO Ingredients (IngredientName) VALUES ("Onion");

-- Grilled Buffalo Chicken Ranch Tacos

INSERT INTO Ingredients (IngredientName) VALUES ("Chicken Thighs");
INSERT INTO Ingredients (IngredientName) VALUES ("Seasoned Salt");
INSERT INTO Ingredients (IngredientName) VALUES ("Chipotle Chili Powder");
INSERT INTO Ingredients (IngredientName) VALUES ("Buffalo Sauce");
INSERT INTO Ingredients (IngredientName) VALUES ("Hard Shell Tacos");
INSERT INTO Ingredients (IngredientName) VALUES ("Shredded Mexican Cheese Blend");
INSERT INTO Ingredients (IngredientName) VALUES ("Shredded Lettuce");
INSERT INTO Ingredients (IngredientName) VALUES ("Cilantro");
INSERT INTO Ingredients (IngredientName) VALUES ("Green Onion");
INSERT INTO Ingredients (IngredientName) VALUES ("Avacado");
INSERT INTO Ingredients (IngredientName) VALUES ("Sour Cream");
INSERT INTO Ingredients (IngredientName) VALUES ("Mayo");
INSERT INTO Ingredients (IngredientName) VALUES ("Buttermilk");
INSERT INTO Ingredients (IngredientName) VALUES ("Dried Parsley");
INSERT INTO Ingredients (IngredientName) VALUES ("Dried Dill");
INSERT INTO Ingredients (IngredientName) VALUES ("Garlic Powder");
INSERT INTO Ingredients (IngredientName) VALUES ("Onion Powder");
INSERT INTO Ingredients (IngredientName) VALUES ("Pickled Jalapenos");
INSERT INTO Ingredients (IngredientName) VALUES ("Chives");

-- Blueberry Croissant French Toast Bake

INSERT INTO Ingredients (IngredientName) VALUES ("Eggs");
INSERT INTO Ingredients (IngredientName) VALUES ("Maple Syrup");
INSERT INTO Ingredients (IngredientName) VALUES ("Orange Zest");
INSERT INTO Ingredients (IngredientName) VALUES ("Grand Marnier");
INSERT INTO Ingredients (IngredientName) VALUES ("Vanilla Extract");
INSERT INTO Ingredients (IngredientName) VALUES ("Cinnamon");
INSERT INTO Ingredients (IngredientName) VALUES ("Salt");
INSERT INTO Ingredients (IngredientName) VALUES ("Croissants");
INSERT INTO Ingredients (IngredientName) VALUES ("Blueberry Jam");
INSERT INTO Ingredients (IngredientName) VALUES ("Ricotta Cheese");
INSERT INTO Ingredients (IngredientName) VALUES ("Blueberries");

SELECT * FROM INGREDIENTS;


-- Macaroni & Cheese

INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Macaroni & Cheese", 1);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Macaroni & Cheese", 2);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Macaroni & Cheese", 3);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Macaroni & Cheese", 4);

-- Beans & Rice

INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Beans & Rice", 5);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Beans & Rice", 6);

-- Hamburgers

INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 7);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 8);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 9);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 10);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 11);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 12);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 13);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Hamburgers", 14);

-- Grilled Buffalo Ranch Chicken Tacos

INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 15);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 16);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 17);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 18);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 19);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 20);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 21);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 22);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 23);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 24);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 25);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 26);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 27);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 28);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 29);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 30);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 31);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 32);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 33);

-- Blueberry Croissant

INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 34);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 3);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 35);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 36);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 37);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 38);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 39);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 40);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 41);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 42);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 43);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 2);
INSERT INTO Meal (RecipeName, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 44);

SELECT * FROM Cookbook;
SELECT * FROM Recipe;
SELECT * FROM Ingredients;
SELECT * FROM Meal;