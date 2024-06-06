-- Stored Procedures to get information

-- Get the ingredients in a meal

DROP PROCEDURE IF EXISTS GetMealIngredients;

DELIMITER $$

CREATE PROCEDURE GetMealIngredients (myRecipeName varchar(100))

BEGIN
  SELECT Ingredients.IngredientName
  FROM Meal JOIN Ingredients ON Meal.IngredientId = Ingredients.Id
  WHERE Meal.RecipeName = myRecipeName
  ORDER BY Ingredients.IngredientName;
END $$
DELIMITER ;

-- Get the name of all cookbooks in the database

DROP PROCEDURE IF EXISTS GetAllCookbookNames;

DELIMITER $$

CREATE PROCEDURE GetAllCookbookNames ()

BEGIN
  SELECT CookbookName
  FROM Cookbook;
END $$
DELIMITER ;

-- Get the information known about a cookbook

DROP PROCEDURE IF EXISTS GetCookbookInfo;

DELIMITER $$

CREATE PROCEDURE GetCookbookInfo(myCookbookName varchar(200))

BEGIN
  SELECT *
  FROM Cookbook
  WHERE CookbookName = myCookbookName;
END $$
DELIMITER ;

-- Get all recipe names

DROP PROCEDURE IF EXISTS GetAllRecipeNames;

DELIMITER $$

CREATE PROCEDURE GetAllRecipeNames()

BEGIN
  SELECT RecipeName
  FROM Recipe;
END $$
DELIMITER ;

-- Get recipes names from one cookbook

DROP PROCEDURE IF EXISTS GetRecipesFromOneCookbook;

DELIMITER $$

CREATE PROCEDURE GetRecipesFromOneCookbook(myCookbookName varchar(200))

BEGIN
  SELECT RecipeName
  FROM Recipe
  WHERE CookbookName = myCookbookName;
END $$
DELIMITER ;

-- Get the information known about a recipe

DROP PROCEDURE IF EXISTS GetRecipeInfo;

DELIMITER $$

CREATE PROCEDURE GetRecipeInfo(myRecipeName varchar(100))

BEGIN
  SELECT *
  FROM Recipe
  WHERE RecipeName = myRecipeName;
END $$
DELIMITER ;