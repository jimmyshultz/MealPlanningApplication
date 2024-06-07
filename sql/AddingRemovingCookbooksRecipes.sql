USE MealPlanning;

-- Create Cookbook

DROP PROCEDURE IF EXISTS AddCookbook;

DELIMITER $$

CREATE PROCEDURE AddCookbook (
    myCookbook VARCHAR(200),
    myIsBook BOOL,
    myWebsite VARCHAR(200)
)
BEGIN
    DECLARE cookbookCount INT;

    -- Check if the cookbook already exists
    SELECT COUNT(*) INTO cookbookCount
    FROM Cookbook
    WHERE CookbookName = myCookbook;

    -- If the cookbook does not exist, add it
    IF cookbookCount = 0 THEN
        INSERT INTO Cookbook (CookbookName, IsBook, Website)
        VALUES (myCookbook, myIsBook, myWebsite);
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
    myCookbook VARCHAR(200)
)
BEGIN
    DECLARE cookbookCount INT;

    -- Check if the cookbook exists
    SELECT COUNT(*) INTO cookbookCount
    FROM Cookbook
    WHERE CookbookName = myCookbook;

    -- If the cookbook exists, delete it
    IF cookbookCount > 0 THEN
        DELETE FROM Cookbook
        WHERE CookbookName = myCookbook;
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
    newWebsite VARCHAR(200)
    
)
BEGIN
    DECLARE bookCount INT;

    -- Check if the cookbook exists
    SELECT COUNT(*) INTO bookCount
    FROM cookbook
    WHERE CookbookName = myCookbook;

    -- If the cookbook exists, update its information
    IF bookCount > 0 THEN
        UPDATE cookbook
        SET CookbookName = newCookbookName,
            IsBook = newIsBook,
            Website = newWebsite
        WHERE CookbookName = myCookbook;
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
    myServings INT
)
BEGIN
    DECLARE recipeCount INT;

    -- Check if the recipe already exists
    SELECT COUNT(*) INTO recipeCount
    FROM Recipe
    WHERE RecipeName = myRecipe AND CookbookName = myCookbook;

    -- If the recipe does not exist, add it
    IF recipeCount = 0 THEN
        INSERT INTO Recipe (RecipeName, CookbookName, TotalServings)
        VALUES (myRecipe, myCookbook, myServings);
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
    IN myRecipe VARCHAR(100)
)
BEGIN
    DECLARE recipeCount INT;

    -- Check if the recipe exists
    SELECT COUNT(*) INTO recipeCount
    FROM Recipe
    WHERE RecipeName = myRecipe;

    -- If the recipe exists, delete it
    IF recipeCount > 0 THEN
        DELETE FROM Recipe
        WHERE RecipeName = myRecipe;
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
    newServings INT
)
BEGIN
    DECLARE recipeCount INT;

    -- Check if the recipe exists
    SELECT COUNT(*) INTO recipeCount
    FROM recipe
    WHERE RecipeName = myRecipe;

    -- If the recipe exists, update its information
    IF recipeCount > 0 THEN
        UPDATE recipe
        SET RecipeName = newRecipeName,
            CookbookName = newCookbookName,
            TotalServings = newServings
        WHERE RecipeName = myRecipe;
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
    myIngredient VARCHAR(100)
)
BEGIN
    DECLARE ingredientCount INT;

    -- Check if the ingredient already exists
    SELECT COUNT(*) INTO ingredientCount
    FROM Ingredients
    WHERE IngredientName = myIngredient;

    -- If the ingredient does not exist, add it
    IF ingredientCount = 0 THEN
        INSERT INTO Ingredients (IngredientName)
        VALUES (myIngredient);
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
    myIngredient VARCHAR(100)
)
BEGIN
    DECLARE ingredientCount INT;

    -- Check if the ingredient exists
    SELECT COUNT(*) INTO ingredientCount
    FROM Ingredients
    WHERE IngredientName = myIngredient;

    -- If the ingredient exists, delete it
    IF ingredientCount > 0 THEN
        DELETE FROM Ingredients
        WHERE IngredientName = myIngredient;
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
    newIngredientName VARCHAR(100)
)
BEGIN
    DECLARE ingredientCount INT;

    -- Check if the ingredient exists
    SELECT COUNT(*) INTO ingredientCount
    FROM ingredients
    WHERE IngredientName = myIngredient;

    -- If the recipe exists, update its information
    IF ingredientCount > 0 THEN
        UPDATE ingredients
        SET IngredientName = newIngredientName
        WHERE IngredientName = myIngredient;
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
    myRecipe VARCHAR(100)
)
BEGIN
    DECLARE pairingCount INT;
    DECLARE myIngredientId INT;
    
    -- Get the ID associated to the ingredient name
    SELECT Id INTO myIngredientId
    FROM Ingredients
    WHERE IngredientName = myIngredient;
    
    IF myIngredientId IS NULL THEN
        -- Handle the case where the ingredient does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ingredient does not exist';
    ELSE
		-- Check if the pairing exists
        SELECT COUNT(*) INTO pairingCount
        FROM meal
        WHERE IngredientId = myIngredientId and RecipeName = myRecipe;

        -- If the pairing doesn't exists, add it to the meal relation
        IF pairingCount = 0 THEN
            INSERT INTO Meal (RecipeName, IngredientId)
            VALUES (myRecipe, myIngredientId);
        ELSE
            -- Handle the case where the pairing already exists
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Pairing already exists';
		END IF;        
    END IF;
END $$

DELIMITER ;