DROP DATABASE IF EXISTS MealPlanning;

CREATE DATABASE MealPlanning;

USE  MealPlanning;

CREATE TABLE IF NOT EXISTS Users (
UserId INT auto_increment NOT NULL,
Email VARCHAR(100) NOT NULL UNIQUE,
PasswordHash VARCHAR(255),
FirstName VARCHAR(50),
LastName VARCHAR(50),
GoogleId VARCHAR(100) UNIQUE,
FacebookId VARCHAR(100) UNIQUE,
PRIMARY KEY (UserId)
);

CREATE TABLE IF NOT EXISTS Cookbook (
CookbookName varchar(200) not null,
IsBook bool not null,
Website varchar(200),
UserId int NOT NULL,
PRIMARY KEY (CookbookName, UserId),
FOREIGN KEY (UserId) REFERENCES Users (UserId) ON UPDATE CASCADE ON DELETE CASCADE,
UNIQUE (CookbookName, UserId)
);

CREATE TABLE IF NOT EXISTS Recipe (
    RecipeName varchar(100) NOT NULL,
    CookbookName varchar(200),
    TotalServings int,
    IsOnline bool not null,
    WebpageLink varchar(255),
    UserId int NOT NULL,
    PRIMARY KEY (RecipeName, UserId),
    FOREIGN KEY (CookbookName) REFERENCES Cookbook (CookbookName) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (UserId) REFERENCES Users (UserId) ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE (RecipeName, UserId)
);

CREATE TABLE IF NOT EXISTS Ingredients (
Id int not null auto_increment,
IngredientName varchar(100) not null,
UserId int NOT NULL,
PRIMARY KEY (Id),
FOREIGN KEY (UserId) REFERENCES Users (UserId) ON UPDATE CASCADE ON DELETE CASCADE,
UNIQUE (IngredientName, UserId)
);

CREATE TABLE IF NOT EXISTS Meal (
    RecipeName varchar(100) NOT NULL,
    UserID int NOT NULL,
    IngredientId int NOT NULL,
    PRIMARY KEY (RecipeName, UserID, IngredientId),
    FOREIGN KEY (RecipeName, UserID) REFERENCES Recipe (RecipeName, UserID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (IngredientId) REFERENCES Ingredients (Id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Preliminary data

INSERT INTO Users (Email, PasswordHash, FirstName, LastName) VALUES ("admin@admin.org", "admin", "Admin", "Admin");

INSERT INTO Cookbook (CookbookName, IsBook, UserId) VALUES ("Easy Meals", true, 1);
INSERT INTO Cookbook (CookbookName, IsBook, UserId) VALUES ("Dinner Staples", true, 1);
INSERT INTO Cookbook (CookbookName, IsBook, Website, UserId) VALUES ("Half Baked Harvest - Mains", false, "https://www.halfbakedharvest.com/category/recipes/type-of-meal/main-course/", 1);
INSERT INTO Cookbook (CookbookName, IsBook, Website, UserId) VALUES ("Half Baked Harvest - Brunch", false, "https://www.halfbakedharvest.com/category/recipes/type-of-meal/brunch/", 1);

INSERT INTO Recipe (RecipeName, CookbookName, TotalServings, IsOnline, UserId) VALUES ("Macaroni & Cheese", "Easy Meals", 2, false, 1);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings, IsOnline, UserId) VALUES ("Beans & Rice", "Easy Meals", 2, false, 1);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings, IsOnline, UserId) VALUES ("Hamburgers", "Dinner Staples", 4, false, 1);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings, IsOnline, WebpageLink, UserId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", "Half Baked Harvest - Mains", 6, true, "https://www.halfbakedharvest.com/grilled-buffalo-ranch-chicken-tacos/", 1);
INSERT INTO Recipe (RecipeName, CookbookName, TotalServings, IsOnline, WebpageLink, UserId) VALUES ("Blueberry Croissant French Toast Bake", "Half Baked Harvest - Brunch", 6, true, "https://www.halfbakedharvest.com/blueberry-croissant-french-toast-bake/", 1);

-- Macaroni and Cheese

INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Macaroni", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Butter", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Milk", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Cheese Powder", 1);

-- Beans and Rice

INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Black Beans", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("White Rice", 1);

-- Hamburgers

INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Beef Patties", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Tomato", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Lettuce", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Hamburger Buns", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Ketchup", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Mustard", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Pickles", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Onion", 1);

-- Grilled Buffalo Chicken Ranch Tacos

INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Chicken Thighs", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Seasoned Salt", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Chipotle Chili Powder", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Buffalo Sauce", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Hard Shell Tacos", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Shredded Mexican Cheese Blend", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Shredded Lettuce", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Cilantro", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Green Onion", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Avacado", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Sour Cream", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Mayo", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Buttermilk", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Dried Parsley", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Dried Dill", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Garlic Powder", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Onion Powder", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Pickled Jalapenos", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Chives", 1);

-- Blueberry Croissant French Toast Bake

INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Eggs", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Maple Syrup", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Orange Zest", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Grand Marnier", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Vanilla Extract", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Cinnamon", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Salt", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Croissants", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Blueberry Jam", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Ricotta Cheese", 1);
INSERT INTO Ingredients (IngredientName, UserId) VALUES ("Blueberries", 1);

-- Macaroni & Cheese

INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Macaroni & Cheese", 1, 1);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Macaroni & Cheese", 1, 2);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Macaroni & Cheese", 1, 3);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Macaroni & Cheese", 1, 4);

-- Beans & Rice

INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Beans & Rice", 1, 5);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Beans & Rice", 1, 6);

-- Hamburgers

INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 7);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 8);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 9);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 10);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 11);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 12);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 13);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Hamburgers", 1, 14);

-- Grilled Buffalo Ranch Chicken Tacos

INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 15);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 16);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 17);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 18);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 19);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 20);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 21);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 22);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 23);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 24);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 25);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 26);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 27);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 28);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 29);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 30);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 31);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 32);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Grilled Buffalo Ranch Chicken Tacos", 1, 33);

-- Blueberry Croissant

INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 34);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 3);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 35);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 36);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 37);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 38);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 39);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 40);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 41);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 42);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 43);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 2);
INSERT INTO Meal (RecipeName, UserId, IngredientId) VALUES ("Blueberry Croissant French Toast Bake", 1, 44);

SELECT * FROM Users;
SELECT * FROM Cookbook;
SELECT * FROM Recipe;
SELECT * FROM Ingredients;
SELECT * FROM Meal;