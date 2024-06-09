/**
 * Represents a cache object.
 * @class
 */
class Cache {
  constructor() {
    this.cookbookNames;
    this.recipeNames;
  }
}

//object to hold the string of a recipe name for each day of the week

/**
 * Represents a weekly meal plan.
 * @class
 */
class WeeklyMealPlan {
    constructor() {
      this.monday = "";
      this.tuesday = "";
      this.wednesday = "";
      this.thursday = "";
      this.friday = "";
      this.saturday = "";
      this.sunday = "";
    }
  
    setMonday(recipe) {
      this.monday = recipe;
    }
  
    setTuesday(recipe) {
      this.tuesday = recipe;
    }
  
    setWednesday(recipe) {
      this.wednesday = recipe;
    }
  
    setThursday(recipe) {
      this.thursday = recipe;
    }
  
    setFriday(recipe) {
      this.friday = recipe;
    }
  
    setSaturday(recipe) {
      this.saturday = recipe;
    }
  
    setSunday(recipe) {
      this.sunday = recipe;
    }
  
    getMonday() {
      return this.monday;
    }
  
    getTuesday() {
      return this.tuesday;
    }
  
    getWednesday() {
      return this.wednesday;
    }
  
    getThursday() {
      return this.thursday;
    }
  
    getFriday() {
      return this.friday;
    }
  
    getSaturday() {
      return this.saturday;
    }
  
    getSunday() {
      return this.sunday;
    }
  }

//initialize objects
let myMealPlan = new WeeklyMealPlan();
let myCache = new Cache();
let serverDomain = 'http://localhost:50051'
getCookbookNames();
getAllRecipeNames();





// Display Functions

// function to display all recipe names in browser

function displayRecipeNames() {
  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = ''; // Clear the display area

  let recipeNamesHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  recipeNamesHTML += '<h5 class="card-title">Recipe Names</h5>';
  recipeNamesHTML += '<ul class="list-group list-group-flush" id="recipe-list">';
  for (let i = 0; i < myCache.recipeNames.length; i++) {
    recipeNamesHTML += `<li class="list-group-item"><a href="#" class="text-decoration-none" data-recipe-name="${myCache.recipeNames[i]}">${myCache.recipeNames[i]}</a></li>`;
  }
  recipeNamesHTML += '</ul>';
  recipeNamesHTML += `<button class="btn btn-primary mt-3" id="add-recipe">Add Recipe</button>`;
  recipeNamesHTML += '</div></div></div>';
  displayArea.innerHTML = recipeNamesHTML;

  // Attach event listeners
  document.getElementById('add-recipe').addEventListener('click', displayAddRecipeForm);
  let recipeLinks = document.querySelectorAll('#recipe-list a');
  recipeLinks.forEach(link => {
    link.addEventListener('click', function(event) {
      event.preventDefault();
      getRecipeInfo(this.dataset.recipeName);
    });
  });
}

// function to display recipe info for selected recipe

function displayRecipeInfo(data, recipe_name) {
  let recipeInfoHTML = `<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">`;
  recipeInfoHTML += `<h5 class="card-title" id="recipe-name">${recipe_name}</h5>`;
  recipeInfoHTML += `<p class="card-text">${data.message}</p>`;
  recipeInfoHTML += '<ul class="list-group list-group-flush mb-3" id="ingredient-list">';
  for (let i = 0; i < data.ingredients.length; i++) {
    recipeInfoHTML += `<li class="list-group-item"><a href="#" class="text-decoration-none" data-ingredient="${data.ingredients[i]}">${data.ingredients[i]}</a></li>`;
  }
  recipeInfoHTML += '</ul>';
  recipeInfoHTML += `<button class="btn btn-primary mb-3" id="add-ingredient" data-recipe-name="${recipe_name}">Add Ingredient</button>`;

  // create a selector to assign recipe to a day of the week
  recipeInfoHTML += `<form id="meal-plan-assignment-form">`
  recipeInfoHTML += `<p>Add ${recipe_name} to Weekly Meal Plan: </p>`
  recipeInfoHTML += `<div class="input-group mb-3">`
  recipeInfoHTML += `<select class="form-select" id="day-of-week" name="day-of-week">`
  recipeInfoHTML += `<option value="Monday">Monday</option>`
  recipeInfoHTML += `<option value="Tuesday">Tuesday</option>`
  recipeInfoHTML += `<option value="Wednesday">Wednesday</option>`
  recipeInfoHTML += `<option value="Thursday">Thursday</option>`
  recipeInfoHTML += `<option value="Friday">Friday</option>`
  recipeInfoHTML += `<option value="Saturday">Saturday</option>`
  recipeInfoHTML += `<option value="Sunday">Sunday</option>`
  recipeInfoHTML += `</select><button class="btn btn-secondary" type="submit">Assign</button></div></form>`

  recipeInfoHTML += `<br><button class="btn btn-danger" id="delete-recipe" data-recipe-name="${recipe_name}">Delete Recipe</button>`;
  recipeInfoHTML += `</div></div></div>`;

  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = recipeInfoHTML;

  // Attach event listeners
  document.getElementById('add-ingredient').addEventListener('click', function() {
    displayAddIngredientForm(this.dataset.recipeName);
  });
  document.getElementById('delete-recipe').addEventListener('click', function() {
    deleteRecipe(this.dataset.recipeName);
  });
  document.getElementById('meal-plan-assignment-form').addEventListener('submit', assignRecipeToDay);
  let ingredientLinks = document.querySelectorAll('#ingredient-list a');
  ingredientLinks.forEach(link => {
    link.addEventListener('click', function(event) {
      event.preventDefault();
      displayIngredient(this.dataset.ingredient);
    });
  });
}

// function to refresh html table displaying recipes and days of the week
function refreshMealPlanTable() {
  let mondayMeal = myMealPlan.getMonday();
  let tuesdayMeal = myMealPlan.getTuesday();
  let wednesdayMeal = myMealPlan.getWednesday();
  let thursdayMeal = myMealPlan.getThursday();
  let fridayMeal = myMealPlan.getFriday();
  let saturdayMeal = myMealPlan.getSaturday();
  let sundayMeal = myMealPlan.getSunday();

  let mondayDisplay = document.getElementById('monday-meal');
  let tuesdayDisplay = document.getElementById('tuesday-meal');
  let wednesdayDisplay = document.getElementById('wednesday-meal');
  let thursdayDisplay = document.getElementById('thursday-meal');
  let fridayDisplay = document.getElementById('friday-meal');
  let saturdayDisplay = document.getElementById('saturday-meal');
  let sundayDisplay = document.getElementById('sunday-meal');

  mondayDisplay.innerText = mondayMeal;
  tuesdayDisplay.innerText = tuesdayMeal;
  wednesdayDisplay.innerText = wednesdayMeal;
  thursdayDisplay.innerText = thursdayMeal;
  fridayDisplay.innerText = fridayMeal;
  saturdayDisplay.innerText = saturdayMeal;
  sundayDisplay.innerText = sundayMeal;
}

// function to display cookbook names in browser

function displayCookbookNames() {
  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = ''; // Clear the display area

  let cookbookNamesHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  cookbookNamesHTML += '<h5 class="card-title">Cookbook Names</h5>';
  cookbookNamesHTML += '<ul class="list-group list-group-flush" id="cookbook-list">';
  for (let i = 0; i < myCache.cookbookNames.length; i++) {
    cookbookNamesHTML += `<li class="list-group-item"><a href="#" class="text-decoration-none" data-cookbook-name="${myCache.cookbookNames[i]}">${myCache.cookbookNames[i]}</a></li>`;
  }
  cookbookNamesHTML += '</ul>';
  cookbookNamesHTML += `<button class="btn btn-primary mt-3" id="add-cookbook">Add Cookbook</button>`;
  cookbookNamesHTML += '</div></div></div>';
  displayArea.innerHTML = cookbookNamesHTML;

  // Attach event listeners
  document.getElementById('add-cookbook').addEventListener('click', displayAddCookbookForm);
  let cookbookLinks = document.querySelectorAll('#cookbook-list a');
  cookbookLinks.forEach(link => {
    link.addEventListener('click', function(event) {
      event.preventDefault();
      getCookbookInfo(this.dataset.cookbookName);
    });
  });
}

// function to display cookbook info in browser

function displayCookbookInfo(data, cookbook_name) {
  let cookbookInfoHTML = `<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">`;
  cookbookInfoHTML += `<h5 class="card-title">${cookbook_name}</h5>`;
  cookbookInfoHTML += `<p class="card-text">${data.message}</p>`;
  cookbookInfoHTML += `<p class="card-text">Recipes: </p>`;
  cookbookInfoHTML += '<ul class="list-group list-group-flush mb-3" id="recipe-list">';
  for (let i = 0; i < data.recipes.length; i++) {
    cookbookInfoHTML += `<li class="list-group-item"><a href="#" class="text-decoration-none" data-recipe-name="${data.recipes[i]}">${data.recipes[i]}</a></li>`;
  }
  cookbookInfoHTML += '</ul>';
  cookbookInfoHTML += `<button class="btn btn-danger" id="delete-cookbook" data-cookbook-name="${cookbook_name}">Delete Cookbook</button>`;
  cookbookInfoHTML += `</div></div></div>`;
  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = cookbookInfoHTML;

  // Attach event listeners
  document.getElementById('delete-cookbook').addEventListener('click', function() {
    deleteCookbook(this.dataset.cookbookName);
  });
  let recipeLinks = document.querySelectorAll('#recipe-list a');
  recipeLinks.forEach(link => {
    link.addEventListener('click', function(event) {
      event.preventDefault();
      getRecipeInfo(this.dataset.recipeName);
    });
  });
}

// function to return to blank display data
function displayBlank() {
  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = "";
}

// display a form to add a custom cookbook
function displayAddCookbookForm() {
  let formHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  formHTML += '<h5 class="card-title">Add a Cookbook</h5>';
  formHTML += '<form id="add-cookbook-form" class="mb-3">';
  formHTML += '<div class="mb-3"><label for="cookbook_name" class="form-label">Cookbook Name:</label>';
  formHTML += '<input type="text" class="form-control" id="cookbook_name" name="cookbook_name"></div>';
  formHTML += '<div class="mb-3"><label for="is_book" class="form-label">Is this a physical book?</label><br>';
  formHTML += '<div class="form-check form-check-inline">';
  formHTML += '<input class="form-check-input" type="radio" id="is_book_yes" name="is_book" value="yes">';
  formHTML += '<label class="form-check-label" for="is_book_yes">Yes</label></div>';
  formHTML += '<div class="form-check form-check-inline">';
  formHTML += '<input class="form-check-input" type="radio" id="is_book_no" name="is_book" value="no">';
  formHTML += '<label class="form-check-label" for="is_book_no">No</label></div></div>';
  formHTML += '<div class="mb-3"><label for="website" class="form-label">Website (if applicable):</label>';
  formHTML += '<input type="url" class="form-control" id="website" name="website"></div>';
  formHTML += '<button type="submit" class="btn btn-primary">Add Cookbook</button></form>';
  formHTML += '</div></div></div>';

  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('add-cookbook-form').addEventListener('submit', handleAddCookbookSubmit);
}

// display a form to add a custom recipe
function displayAddRecipeForm() {
  let formHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  formHTML += '<h5 class="card-title">Add a Recipe</h5>';
  formHTML += '<form id="add-recipe-form" class="mb-3">';
  formHTML += '<div class="mb-3"><label for="recipe_name" class="form-label">Recipe Name:</label>';
  formHTML += '<input type="text" class="form-control" id="recipe_name" name="recipe_name"></div>';
  formHTML += '<div class="mb-3"><label for="cookbook_name" class="form-label">Cookbook Name:</label>';
  formHTML += '<select class="form-select" id="cookbook_name" name="cookbook_name">';
  for (let i = 0; i < myCache.cookbookNames.length; i++) {
    formHTML += `<option value="${myCache.cookbookNames[i]}">${myCache.cookbookNames[i]}</option>`;
  }
  formHTML += '</select></div>';
  formHTML += '<div class="mb-3"><label for="servings" class="form-label">Number of Servings:</label>';
  formHTML += '<select class="form-select" id="servings" name="servings">';
  for (let i = 1; i <= 20; i++) {
    formHTML += `<option value="${i}">${i}</option>`;
  }
  formHTML += '</select></div>';
  formHTML += '<button type="submit" class="btn btn-primary">Add Recipe</button></form>';
  formHTML += '</div></div></div>';

  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('add-recipe-form').addEventListener('submit', handleAddRecipeSubmit);
}

// display a form to add a custom ingredient
function displayAddIngredientForm(recipe_name) {
  let formHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  formHTML += `<h5 class="card-title">Add an Ingredient to <span id="recipe-name">${recipe_name}</span></h5>`;
  formHTML += '<form id="add-ingredient-form" class="mb-3">';
  formHTML += '<div class="mb-3"><label for="ingredient-name" class="form-label">Ingredient:</label>';
  formHTML += '<input type="text" class="form-control" id="ingredient-name" name="ingredient-name"></div>';
  formHTML += '<button type="submit" class="btn btn-primary">Add Ingredient</button></form>';
  formHTML += '</div></div></div>';

  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('add-ingredient-form').addEventListener('submit', handleAddIngredientSubmit);
}

// display ingredient name and a button to delete ingredient

function displayIngredient(ingredient_name) {
  let ingredientHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  ingredientHTML += `<p class="card-text">${ingredient_name}</p>`;
  ingredientHTML += `<button class="btn btn-danger" id="delete-ingredient" data-ingredient-name="${ingredient_name}">Delete Ingredient</button>`;
  ingredientHTML += '</div></div></div>';

  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = ingredientHTML;

  // Attach event listener
  document.getElementById('delete-ingredient').addEventListener('click', function() {
    deleteIngredient(this.dataset.ingredientName);
  });
}

// display a page to register a new user

function displayRegisterForm() {
  let formHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  formHTML += '<h5 class="card-title">Register</h5>';
  formHTML += '<form id="register-form" class="mb-3">';
  formHTML += '<div class="mb-3"><label for="email" class="form-label">Email:</label>';
  formHTML += '<input type="email" class="form-control" id="email" name="email"></div>';
  formHTML += '<div class="mb-3"><label for="password" class="form-label">Password:</label>';
  formHTML += '<input type="password" class="form-control" id="password" name="password"></div>';
  formHTML += '<div class="mb-3"><label for="first_name" class="form-label">First Name:</label>';
  formHTML += '<input type="text" class="form-control" id="first_name" name="first_name"></div>';
  formHTML += '<div class="mb-3"><label for="last_name" class="form-label">Last Name:</label>';
  formHTML += '<input type="text" class="form-control" id="last_name" name="last_name"></div>';
  formHTML += '<button type="submit" class="btn btn-primary">Register</button></form>';
  formHTML += '</div></div></div>';

  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    let firstName = document.getElementById('first_name').value;
    let lastName = document.getElementById('last_name').value;
    addUser(email, password, firstName, lastName);
  });
}

// display a page to login

function displayLoginForm() {
  let formHTML = '<div class="col-lg-6 mx-auto mb-4"><div class="card"><div class="card-body">';
  formHTML += '<h5 class="card-title">Login</h5>';
  formHTML += '<form id="login-form" class="mb-3">';
  formHTML += '<div class="mb-3"><label for="email" class="form-label">Email:</label>';
  formHTML += '<input type="email" class="form-control" id="email" name="email"></div>';
  formHTML += '<div class="mb-3"><label for="password" class="form-label">Password:</label>';
  formHTML += '<input type="password" class="form-control" id="password" name="password"></div>';
  formHTML += '<button type="submit" class="btn btn-primary">Login</button></form>';
  formHTML += '</div></div></div>';

  const displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    login(email, password);
  });

}

function displayEmailInNav(email) {
  userSectionHTML = `<ul class="navbar-nav ms-auto" id="nav-user-section"><li class="nav-item"><a class="nav-link" href="#" id="user" onclick="#">Hello, ${email}</a></li></ul>`;
  document.getElementById('nav-user-section').innerHTML = userSectionHTML;
}

//Server Communication Functions

//function to get recipe names from database through the backend server

/**
 * Retrieves all recipe names from the server and stores them in the global `myCache` object.
 * @returns {Promise} A promise that resolves to undefined when the function completes.
 */
async function getAllRecipeNames() {
  console.log("Trying to get recipe names from 'localhost:50051'");
  fetch(`http://localhost:50051/all_recipe_names`)
      .then(response => { return response.json() })
      .then(data => { 
            console.log("Data from server:", data);
            myCache.recipeNames = data;
            console.log(myCache.recipeNames) })
      .catch((error) => { console.log(error) })
}

//function to get recipe info for selected recipe

async function getRecipeInfo(recipe_name) {
  console.log(`Trying to get recipe info from 'localhost:50051' for ${recipe_name}`);
  fetch(`http://localhost:50051/recipe_info/${recipe_name}`)
      .then(response => { return response.json() })
      .then(data => { 
            displayRecipeInfo(data, recipe_name);
          })
      .catch((error) => { console.log(error) })
}

//function to get cookbook names from db through the backend server

async function getCookbookNames() {
  console.log("Trying to get cookbook names from 'localhost:50051'");
  fetch(`http://localhost:50051/cookbook_names`)
      .then(response => { return response.json() })
      .then(data => { 
            console.log("Data from server:", data);
            myCache.cookbookNames = data;
            console.log(myCache.cookbookNames) })
      .catch((error) => { console.log(error) })
}

//function to get cookbook info for selected cookbook

async function getCookbookInfo(encoded_name) {
  let cookbook_name = decodeURIComponent(encoded_name);
  console.log(`Trying to get cookbook info from 'localhost:50051' for ${cookbook_name}`);
  fetch(`http://localhost:50051/cookbook_info/${cookbook_name}`)
      .then(response => { return response.json() })
      .then(data => { 
            displayCookbookInfo(data, cookbook_name);
          })
      .catch((error) => { console.log(error) })
}

//add a cookbook to the database on cookbooks view

async function addCookbook(cookbook_name, isBook, website) {
  console.log(`Trying to add cookbook ${cookbook_name} to database through 'localhost:50051'`);
  let new_cookbook_info = {new_cookbook_name: cookbook_name, new_is_book: isBook, new_website: website}

  try {
    const response = await fetch(`${serverDomain}/add_cookbook`, {
      method: 'PUT', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(new_cookbook_info)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data);
  } catch (error) {
    console.error('Error adding cookbook:', error);
  }
  getCookbookNames();
  displayBlank();
}

//remove a cookbook from the database on cookbook info view

async function deleteCookbook(cookbook_name) {
  console.log(`Trying to delete cookbook ${cookbook_name} from database through 'localhost:50051'`);

  try {
    const response = await fetch(`${serverDomain}/delete_cookbook/${cookbook_name}`, {
      method: 'DELETE', 
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data);
  } catch (error) {
    console.error('Error deleting cookbook:', error);
  }
  getCookbookNames();
  getAllRecipeNames();
  displayBlank();
}

//add a recipe to the database on cookbook info view

async function addRecipe(recipe_name, cookbook_name, servings) {
  console.log(`Trying to add recipe ${recipe_name} to database through 'localhost:50051'`);
  let new_recipe_info = {new_recipe_name: recipe_name, new_cookbook_name: cookbook_name, new_servings: servings}

  try {
    const response = await fetch(`${serverDomain}/add_recipe`, {
      method: 'PUT', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(new_recipe_info)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data);
    getAllRecipeNames();
  } catch (error) {
    console.error('Error adding recipe:', error);
  }
  displayBlank();
}

//remove a recipe from the database on recipe info view

async function deleteRecipe(recipe_name) {
  console.log(`Trying to delete recipe ${recipe_name} from database through 'localhost:50051'`);

  try {
    const response = await fetch(`${serverDomain}/delete_recipe/${recipe_name}`, {
      method: 'DELETE', 
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data);
    getAllRecipeNames();
  } catch (error) {
    console.error('Error deleting recipe:', error);
  }
  displayBlank();
}

// add an ingredient to the database on recipe info view

async function addIngredient(recipe_name, ingredient) {
  console.log(`Trying to add ingredient ${ingredient} to recipe ${recipe_name} in database through 'localhost:50051'`);
  let new_ingredient_info = {new_ingredient: ingredient, recipe: recipe_name}

  try {
    const response = await fetch(`${serverDomain}/add_ingredient`, {
      method: 'PUT', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(new_ingredient_info)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data);
  } catch (error) {
    console.error('Error adding ingredient:', error);
  }
  addIngredientRecipePairing(recipe_name, ingredient);
  getRecipeInfo(recipe_name);
}

//tie an ingredient to a recipe in the database
async function addIngredientRecipePairing(recipe_name, ingredient) {
  console.log(`Trying to add ingredient ${ingredient} to recipe ${recipe_name} in database through 'localhost:50051'`);
  let new_ingredient_info = {ingredient_name: ingredient, recipe_name: recipe_name}

  try {
    const response = await fetch(`${serverDomain}/add_ingredient_recipe_pairing`, {
      method: 'PUT', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(new_ingredient_info)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data);
  } catch (error) {
    console.error('Error adding ingredient-recipe pairing:', error);
  }
  getRecipeInfo(recipe_name);
}

//remove an ingredient from the database on ingredient view
async function deleteIngredient(ingredient_name) {
  console.log(`Trying to delete ingredient ${ingredient_name} from database through 'localhost:50051'`);

  try {
    const response = await fetch(`${serverDomain}/delete_ingredient/${ingredient_name}`, {
      method: 'DELETE', 
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data);
  } catch (error) {
    console.error('Error deleting ingredient:', error);
  }
  displayBlank();
}

//add user to database
async function addUser(email, password, firstName, lastName) {
  console.log("Trying to add user to database through 'localhost:50051'");
  let new_user_info = {
                       email: email,
                       password: password,
                       first_name: firstName,
                       last_name: lastName
                      };
  
  try {
    const response = await fetch(`${serverDomain}/add_user`, {
      method: 'PUT', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(new_user_info)
    });
  
    const data = await response.json()
    console.log(data);

    if (data.success) {
      displayBlank();
    } else {
      console.log(data.success);
      alert("User already exists. Please try again.");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }
  
  } catch (error) {
    console.error('Error adding user:', error);
  }
}

//login user
async function login(email, password) {
  console.log("Trying to login user through 'localhost:50051'");
  let user_info = {
                  email: email,
                  password: password
                  };
  
  try {
    const response = await fetch(`${serverDomain}/login`, {
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(user_info)
    });
  
    const data = await response.json()
    console.log(data);

    if (data.success) {
      alert(`Login with ${email} successful!`);
      displayEmailInNav(email);
      displayBlank();
    } else {
      console.log(data.success);
      alert("Invalid login. Please try again.");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }
  
  } catch (error) {
    console.error('Error logging in:', error);
  }
}


//Event Handling Functions

//handle submit on add cookbook form

function handleAddCookbookSubmit(event) {
  event.preventDefault();
  let cookbook_name = document.getElementById('cookbook_name').value;
  let isBook = document.querySelector('input[name="is_book"]:checked').value === 'yes';
  let website = document.getElementById('website').value;
  addCookbook(cookbook_name, isBook, website);
}

//handle submit on add cookbook form

function handleAddRecipeSubmit(event) {
  event.preventDefault();
  let recipe_name = document.getElementById('recipe_name').value;
  let cookbook_name = document.getElementById('cookbook_name').value;
  let servings = parseInt(document.getElementById('servings').value, 10)
  addRecipe(recipe_name, cookbook_name, servings);
}

//handle submit on add ingredient form

function handleAddIngredientSubmit(event) {
  event.preventDefault();
  let recipe_name = document.getElementById('recipe-name').innerText;
  let ingredient_name = document.getElementById('ingredient-name').value;
  addIngredient(recipe_name, ingredient_name);
}

//function to assign recipe to day of the week in client-side object

function assignRecipeToDay(event) {
  event.preventDefault();

  var recipe_name = document.getElementById('recipe-name').innerText;
  var day_of_week = document.getElementById('day-of-week').value;

  if (day_of_week == 'Monday') {
    myMealPlan.setMonday(recipe_name);
  } else if (day_of_week == 'Tuesday') {
    myMealPlan.setTuesday(recipe_name);
  } else if (day_of_week == 'Wednesday') {
    myMealPlan.setWednesday(recipe_name);
  } else if (day_of_week == 'Thursday') {
    myMealPlan.setThursday(recipe_name);
  } else if (day_of_week == 'Friday') {
    myMealPlan.setFriday(recipe_name);
  } else if (day_of_week == 'Saturday') {
    myMealPlan.setSaturday(recipe_name);
  } else if (day_of_week == 'Sunday') {
    myMealPlan.setSunday(recipe_name);
  }

  refreshMealPlanTable();
}