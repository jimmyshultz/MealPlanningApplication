USE MealPlanning;

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

    -- Check if the cookbook already exists
    SELECT COUNT(*) INTO cookbookCount
    FROM Cookbook
    WHERE CookbookName = myCookbook AND UserId = myUserId;

    -- If the cookbook does not exist, add it
    IF cookbookCount = 0 THEN
        INSERT INTO Cookbook (CookbookName, IsBook, Website, UserId)
        VALUES (myCookbook, myIsBook, myWebsite, myUserId);
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

    -- Check if the recipe already exists
    SELECT COUNT(*) INTO recipeCount
    FROM Recipe
    WHERE RecipeName = myRecipe AND UserId = myUserId AND CookbookName = myCookbook;

    -- If the recipe does not exist, add it
    IF recipeCount = 0 THEN
        INSERT INTO Recipe (RecipeName, CookbookName, TotalServings, IsOnline, WebpageLink, UserId)
        VALUES (myRecipe, myCookbook, myServings, myIsOnline, myWebpageLink, myUserId);
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

    -- Check if the ingredient already exists
    SELECT COUNT(*) INTO ingredientCount
    FROM Ingredients
    WHERE IngredientName = myIngredient AND UserId = myUserId;

    -- If the ingredient does not exist, add it
    IF ingredientCount = 0 THEN
        INSERT INTO Ingredients (IngredientName, UserId)
        VALUES (myIngredient, myUserId);
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