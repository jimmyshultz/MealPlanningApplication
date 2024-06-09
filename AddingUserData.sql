USE MealPlanning;

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

INSERT INTO Users (Email, PasswordHash, FirstName, LastName) VALUES ("jimmy@shultz-kc.com", "greeneighty", "Jimmy", "Shultz");

SELECT * FROM Users;

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

CALL AddUser("jimmy2@shultz-kc.com", "omahaomaha", "Jimmy", "Shultz");

-- Delete User

DROP PROCEDURE IF EXISTS DeleteUser;

DELIMITER $$

CREATE PROCEDURE DeleteUser (
    myEmail VARCHAR(100)
)
BEGIN
    DECLARE userCount INT;

    -- Check if the username exists
    SELECT COUNT(*) INTO userCount
    FROM Users
    WHERE Email = myEmail;

    -- If the cookbook exists, delete it
    IF userCount > 0 THEN
        DELETE FROM Users
        WHERE Email = myEmail;
    ELSE
        -- Optionally handle the case where the username does not exist
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User does not exist';
    END IF;
END $$

DELIMITER ;

CALL DeleteUser("jimmy2@shultz-kc.com");

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

CALL GetUserPassword('test@test.com');

-- Get the User's hashed password

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

CALL GetUserInfo('test@test.com');