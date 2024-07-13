DROP DATABASE IF EXISTS MealPlanning;

CREATE DATABASE MealPlanning;

USE  MealPlanning;

-- Create Relations

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




-- Stored Procedures

-- Get the ingredients in a meal

DROP PROCEDURE IF EXISTS GetMealIngredients;

DELIMITER $$

CREATE PROCEDURE GetMealIngredients (myRecipeName varchar(100), myUserId int)

BEGIN
  SELECT Ingredients.IngredientName
  FROM Meal JOIN Ingredients ON Meal.IngredientId = Ingredients.Id
  WHERE Meal.RecipeName = myRecipeName AND Meal.UserId = myUserId
  ORDER BY Ingredients.IngredientName;
END $$
DELIMITER ;

-- Get the name of all cookbooks in the database

DROP PROCEDURE IF EXISTS GetAllCookbookNames;

DELIMITER $$

CREATE PROCEDURE GetAllCookbookNames (myUserId INT)

BEGIN
  SELECT CookbookName
  FROM Cookbook
  WHERE UserId = myUserId;
END $$
DELIMITER ;

-- Get the information known about a cookbook

DROP PROCEDURE IF EXISTS GetCookbookInfo;

DELIMITER $$

CREATE PROCEDURE GetCookbookInfo(myCookbookName varchar(200), myUserId INT)

BEGIN
  SELECT *
  FROM Cookbook
  WHERE CookbookName = myCookbookName AND UserId = myUserId;
END $$
DELIMITER ;

-- Get all recipe names

DROP PROCEDURE IF EXISTS GetAllRecipeNames;

DELIMITER $$

CREATE PROCEDURE GetAllRecipeNames(myUserId int)

BEGIN
  SELECT RecipeName
  FROM Recipe
  WHERE Recipe.UserId = myUserId;
END $$
DELIMITER ;

-- Get recipes names from one cookbook

DROP PROCEDURE IF EXISTS GetRecipesFromOneCookbook;

DELIMITER $$

CREATE PROCEDURE GetRecipesFromOneCookbook(myCookbookName varchar(200), myUserId int)

BEGIN
  SELECT RecipeName
  FROM Recipe
  WHERE CookbookName = myCookbookName AND Recipe.UserId = myUserId;
END $$
DELIMITER ;

-- Get the information known about a recipe

DROP PROCEDURE IF EXISTS GetRecipeInfo;

DELIMITER $$

CREATE PROCEDURE GetRecipeInfo(myRecipeName varchar(100), myUserId int)

BEGIN
  SELECT *
  FROM Recipe
  WHERE RecipeName = myRecipeName AND UserId = myUserId;
END $$
DELIMITER ;

-- Create Cookbook

DROP PROCEDURE IF EXISTS AddCookbook;

DELIMITER $$

CREATE PROCEDURE AddCookbook (
    myCookbook VARCHAR(200),
    myIsBook BOOL,
    myWebsite VARCHAR(200),
    myUserId INT
)
BEGIN
    DECLARE cookbookCount INT;
    DECLARE userCookbookCount INT;

    -- Check if the cookbook already exists
    SELECT COUNT(*) INTO cookbookCount
    FROM Cookbook
    WHERE CookbookName = myCookbook AND UserId = myUserId;
    
    -- Count the total number of cookbooks for the user
    SELECT COUNT(*) INTO userCookbookCount
    FROM Cookbook
    WHERE UserId = myUserId;

    -- If the cookbook does not exist, add it
    IF cookbookCount = 0 THEN
        IF userCookbookCount < 50 THEN
            INSERT INTO Cookbook (CookbookName, IsBook, Website, UserId)
            VALUES (myCookbook, myIsBook, myWebsite, myUserId);
		ELSE
            -- Handle the case where the user already has 50 cookbooks
        	SIGNAL SQLSTATE '45000'
        	SET MESSAGE_TEXT = 'User has reached the maximum number of cookbooks (50)';
    	END IF;
    ELSE
        -- Optionally handle the case where the cookbook already exists
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cookbook already exists';
    END IF;
END $$

DELIMITER ;

-- Delete Cookbook

DROP PROCEDURE IF EXISTS DeleteCookbook;

DELIMITER $$

CREATE PROCEDURE DeleteCookbook (
    myCookbook VARCHAR(200),
    myUserId INT
)
BEGIN
    DECLARE cookbookCount INT;

    -- Check if the cookbook exists
    SELECT COUNT(*) INTO cookbookCount
    FROM Cookbook
    WHERE CookbookName = myCookbook AND UserId = myUserId;

    -- If the cookbook exists, delete it
    IF cookbookCount > 0 THEN
        DELETE FROM Cookbook
        WHERE CookbookName = myCookbook AND UserId = myUserId;
    ELSE
        -- Optionally handle the case where the cookbook does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cookbook does not exist';
    END IF;
END $$

DELIMITER ;

-- Update Cookbook

DROP PROCEDURE IF EXISTS UpdateCookbook

DELIMITER $$

CREATE PROCEDURE UpdateCookbook(
    myCookbook VARCHAR(200),
    newCookbookName VARCHAR(200),
    newIsBook BOOL,
    newWebsite VARCHAR(200),
    myUserId INT
    
)
BEGIN
    DECLARE bookCount INT;

    -- Check if the cookbook exists
    SELECT COUNT(*) INTO bookCount
    FROM cookbook
    WHERE CookbookName = myCookbook AND UserId = myUserId;

    -- If the cookbook exists, update its information
    IF bookCount > 0 THEN
        UPDATE cookbook
        SET CookbookName = newCookbookName,
            IsBook = newIsBook,
            Website = newWebsite
        WHERE CookbookName = myCookbook AND UserId = myUserId;
    ELSE
        -- Handle the case where the cookbook does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cookbook not found';
    END IF;
END $$

DELIMITER ;

-- Create Recipe

DROP PROCEDURE IF EXISTS AddRecipe;

DELIMITER $$

CREATE PROCEDURE AddRecipe (
    myRecipe VARCHAR(100),
    myCookbook VARCHAR(200),
    myServings INT,
    myIsOnline BOOL,
    myWebpageLink VARCHAR (255),
    myUserId INT
)
BEGIN
    DECLARE recipeCount INT;
    DECLARE userRecipeCount INT;

    -- Check if the recipe already exists
    SELECT COUNT(*) INTO recipeCount
    FROM Recipe
    WHERE RecipeName = myRecipe AND UserId = myUserId AND CookbookName = myCookbook;
    
    -- Count the total number of recipes for the user
    SELECT COUNT(*) INTO userRecipeCount
    FROM Recipe
    WHERE UserId = myUserId;

    -- If the recipe does not exist, add it
    IF recipeCount = 0 THEN
        IF userRecipeCount < 100 THEN
            INSERT INTO Recipe (RecipeName, CookbookName, TotalServings, IsOnline, WebpageLink, UserId)
            VALUES (myRecipe, myCookbook, myServings, myIsOnline, myWebpageLink, myUserId);
		ELSE
            -- Handle the case where the user already has 100 recipes
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'User has reached the maximum number of recipes (100)';
		END IF;
    ELSE
        -- Optionally handle the case where the recipe already exists
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Recipe already exists';
    END IF;
END $$

DELIMITER ;

-- Delete Recipe

DROP PROCEDURE IF EXISTS DeleteRecipe;

DELIMITER $$

CREATE PROCEDURE DeleteRecipe (
    myRecipe VARCHAR(100),
    myUserId INT
)
BEGIN
    DECLARE recipeCount INT;

    -- Check if the recipe exists
    SELECT COUNT(*) INTO recipeCount
    FROM Recipe
    WHERE RecipeName = myRecipe AND UserId = myUserId;

    -- If the recipe exists, delete it
    IF recipeCount > 0 THEN
        DELETE FROM Recipe
        WHERE RecipeName = myRecipe AND UserId = myUserId;
    ELSE
        -- Optionally handle the case where the recipe does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Recipe does not exist';
    END IF;
END $$

DELIMITER ;

-- Update Recipe

DROP PROCEDURE IF EXISTS UpdateRecipe

DELIMITER $$

CREATE PROCEDURE UpdateRecipe(
    myRecipe VARCHAR(200),
    newRecipeName VARCHAR(100),
    newCookbookName VARCHAR(200),
    newServings INT,
    myUserId INT
)
BEGIN
    DECLARE recipeCount INT;

    -- Check if the recipe exists
    SELECT COUNT(*) INTO recipeCount
    FROM recipe
    WHERE RecipeName = myRecipe AND UserId = myUserId;

    -- If the recipe exists, update its information
    IF recipeCount > 0 THEN
        UPDATE recipe
        SET RecipeName = newRecipeName,
            CookbookName = newCookbookName,
            TotalServings = newServings
        WHERE RecipeName = myRecipe AND UserId = myUserId;
    ELSE
        -- Handle the case where the recipe does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Recipe not found';
    END IF;
END $$

DELIMITER ;

-- Create Ingredient

DROP PROCEDURE IF EXISTS AddIngredient;

DELIMITER $$

CREATE PROCEDURE AddIngredient (
    myIngredient VARCHAR(100),
    myUserId INT
)
BEGIN
    DECLARE ingredientCount INT;
    DECLARE userIngredientCount INT;

    -- Check if the ingredient already exists
    SELECT COUNT(*) INTO ingredientCount
    FROM Ingredients
    WHERE IngredientName = myIngredient AND UserId = myUserId;
    
    -- Count the total number of recipes for the user
    SELECT COUNT(*) INTO userIngredientCount
    FROM Ingredients
    WHERE UserId = myUserId;

    -- If the ingredient does not exist, add it
    IF ingredientCount = 0 THEN
        IF userIngredientCount < 500 THEN
            INSERT INTO Ingredients (IngredientName, UserId)
            VALUES (myIngredient, myUserId);
		ELSE
            -- Handle the case where the user already has 500 recipes
        	SIGNAL SQLSTATE '45000'
        	SET MESSAGE_TEXT = 'User has reached the maximum number of ingredients (500)';
    	END IF;
    ELSE
        -- Optionally handle the case where the ingredient already exists
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ingredient already exists';
    END IF;
END $$

DELIMITER ;

-- Delete Ingredient

DROP PROCEDURE IF EXISTS DeleteIngredient;

DELIMITER $$

CREATE PROCEDURE DeleteIngredient (
    myIngredient VARCHAR(100),
    myUserId INT
)
BEGIN
    DECLARE ingredientCount INT;

    -- Check if the ingredient exists
    SELECT COUNT(*) INTO ingredientCount
    FROM Ingredients
    WHERE IngredientName = myIngredient AND UserId = myUserId;

    -- If the ingredient exists, delete it
    IF ingredientCount > 0 THEN
        DELETE FROM Ingredients
        WHERE IngredientName = myIngredient AND UserId = myUserId;
    ELSE
        -- Optionally handle the case where the ingredient does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ingredient does not exist';
    END IF;
END $$

DELIMITER ;

-- Update Ingredient

DROP PROCEDURE IF EXISTS UpdateIngredient;

DELIMITER $$

CREATE PROCEDURE UpdateIngredient(
    myIngredient VARCHAR(100),
    newIngredientName VARCHAR(100),
    myUserId INT
)
BEGIN
    DECLARE ingredientCount INT;

    -- Check if the ingredient exists
    SELECT COUNT(*) INTO ingredientCount
    FROM ingredients
    WHERE IngredientName = myIngredient AND UserId = myUserId;

    -- If the recipe exists, update its information
    IF ingredientCount > 0 THEN
        UPDATE ingredients
        SET IngredientName = newIngredientName
        WHERE IngredientName = myIngredient AND UserId = myUserId;
    ELSE
        -- Handle the case where the ingredient does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ingredient not found';
    END IF;
END $$

DELIMITER ;

-- add ingredient and recipe to meal relation together

DROP PROCEDURE IF EXISTS AddIngredientRecipePairing;

DELIMITER $$

CREATE PROCEDURE AddIngredientRecipePairing(
    myIngredient VARCHAR(100),
    myRecipe VARCHAR(100),
    myUserId INT
)
BEGIN
    DECLARE pairingCount INT;
    DECLARE myIngredientId INT;
    
    -- Get the ID associated to the ingredient name
    SELECT Id INTO myIngredientId
    FROM Ingredients
    WHERE IngredientName = myIngredient AND UserId = myUserId;
    
    IF myIngredientId IS NULL THEN
        -- Handle the case where the ingredient does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ingredient does not exist';
    ELSE
		-- Check if the pairing exists
        SELECT COUNT(*) INTO pairingCount
        FROM meal
        WHERE IngredientId = myIngredientId AND RecipeName = myRecipe AND UserId = myUserId;

        -- If the pairing doesn't exists, add it to the meal relation
        IF pairingCount = 0 THEN
            INSERT INTO Meal (RecipeName, UserId, IngredientId)
            VALUES (myRecipe, myUserId, myIngredientId);
        ELSE
            -- Handle the case where the pairing already exists
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Pairing already exists';
		END IF;        
    END IF;
END $$

DELIMITER ;

-- Add User

DROP PROCEDURE IF EXISTS AddUser;

DELIMITER $$

CREATE PROCEDURE AddUser (
    myEmail VARCHAR(100),
    myPasswordHash VARCHAR(255),
    myFirstName VARCHAR(50),
    myLastName VARCHAR(50)
)
BEGIN
    DECLARE userCount INT;

    -- Check if the email already exists
    SELECT COUNT(*) INTO userCount
    FROM Users
    WHERE Email = myEmail;

    -- If the email does not exist, add it
    IF userCount = 0 THEN
        INSERT INTO Users (Email, PasswordHash, FirstName, LastName)
        VALUES (myEmail, myPasswordHash, myFirstName, myLastName);
    ELSE
        -- Optionally handle the case where the username already exists
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User already exists';
    END IF;
END $$

DELIMITER ;

-- Delete User

DROP PROCEDURE IF EXISTS DeleteUser;

DELIMITER $$

CREATE PROCEDURE DeleteUser (
    myEmail VARCHAR(100)
)
BEGIN
    DECLARE userCount INT;

    -- Check if the user exists
    SELECT COUNT(*) INTO userCount
    FROM Users
    WHERE Email = myEmail;

    -- If the user exists, delete it
    IF userCount > 0 THEN
        DELETE FROM Users
        WHERE Email = myEmail;
    ELSE
        -- Optionally handle the case where the user does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User does not exist';
    END IF;
END $$

DELIMITER ;

-- Get the User's hashed password

DROP PROCEDURE IF EXISTS GetUserPassword;

DELIMITER $$

CREATE PROCEDURE GetUserPassword (
    myEmail VARCHAR(100)
)
BEGIN
    DECLARE userCount INT;

    -- Check if the user exists
    SELECT COUNT(*) INTO userCount
    FROM Users
    WHERE Email = myEmail;

    -- If the user exists return the password hash
    IF userCount > 0 THEN
        SELECT PasswordHash
        FROM Users
        WHERE Email = myEmail;
    ELSE
        -- Optionally handle the case where the user does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User does not exist';
    END IF;
END $$

DELIMITER ;

-- Get the info for the user

DROP PROCEDURE IF EXISTS GetUserInfo;

DELIMITER $$

CREATE PROCEDURE GetUserInfo (
    myEmail VARCHAR(100)
)
BEGIN
    DECLARE userCount INT;

    -- Check if the user exists
    SELECT COUNT(*) INTO userCount
    FROM Users
    WHERE Email = myEmail;

    -- If the user exists return all info
    IF userCount > 0 THEN
        SELECT *
        FROM Users
        WHERE Email = myEmail;
    ELSE
        -- Optionally handle the case where the user does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User does not exist';
    END IF;
END $$

DELIMITER ;

-- Test data

-- Insertion

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

-- Viewing test data

SELECT * FROM Users;
SELECT * FROM Cookbook;
SELECT * FROM Recipe;
SELECT * FROM Ingredients;
SELECT * FROM Meal;