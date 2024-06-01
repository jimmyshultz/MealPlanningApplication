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

//function to display all recipe names in browser

function displayRecipeNames() {
  let recipeNamesHTML = "<ul>";
  for (let i = 0; i < myCache.recipeNames.length; i++) {
    recipeNamesHTML += `<li><a onclick="getRecipeInfo('${myCache.recipeNames[i]}')">${myCache.recipeNames[i]}</a></li>`;
  }
  recipeNamesHTML += "</ul>";
  recipeNamesHTML += `<button id="add-recipe" onclick="displayAddRecipeForm()">Add Recipe</button>`;
  var displayArea = document.getElementById('display-text');
  displayArea.innerHTML = recipeNamesHTML;
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

//function to display recipe info for selected recipe

/**
 * Displays recipe information on the webpage.
 * 
 * @param {object} data - The recipe data.
 * @param {string} recipe_name - The name of the recipe.
 */
function displayRecipeInfo(data, recipe_name) {
  let recipeInfoHTML = `<h3 id="recipe-name">${recipe_name}</h3>`;
  recipeInfoHTML += `<p>${data.message}</p>`;
  recipeInfoHTML += `<ul>`;
  for (let i = 0; i < data.ingredients.length; i++) {
    recipeInfoHTML += `<li><a onclick="displayIngredient('${data.ingredients[i]}')">${data.ingredients[i]}</a></li>`;
  }
  recipeInfoHTML += `</ul>`;

  recipeInfoHTML += `<button id="add-ingredient" onclick="displayAddIngredientForm('${recipe_name}')">Add Ingredient</button><br>`

  //create a selector to assign recipe to a day of the week
  recipeInfoHTML += `<form id="meal-plan-assignment-form">`
  recipeInfoHTML += `<p>Add ${recipe_name} to Weekly Meal Plan: </p>`
  recipeInfoHTML += `<select id="day-of-week" name="day-of-week">`
  recipeInfoHTML += `<option value="Monday">Monday</option>`
  recipeInfoHTML += `<option value="Tuesday">Tuesday</option>`
  recipeInfoHTML += `<option value="Wednesday">Wednesday</option>`
  recipeInfoHTML += `<option value="Thursday">Thursday</option>`
  recipeInfoHTML += `<option value="Friday">Friday</option>`
  recipeInfoHTML += `<option value="Saturday">Saturday</option>`
  recipeInfoHTML += `<option value="Sunday">Sunday</option>`
  recipeInfoHTML += `</select><button type="submit">Assign</button></form>`

  recipeInfoHTML += `<br><button id="delete-recipe" onclick="deleteRecipe('${recipe_name}')">Delete Recipe</button><br>`;

  var displayArea = document.getElementById('display-text');
  displayArea.innerHTML = recipeInfoHTML;

  document.getElementById('meal-plan-assignment-form').addEventListener('submit', assignRecipeToDay);
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

//function to refresh html table displaying recipes and days of the week

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

// function to display cookbook names in browser

function displayCookbookNames() {
  let cookbookNamesHTML = "<ul>";
  for (let i = 0; i < myCache.cookbookNames.length; i++) {
    cookbookNamesHTML += `<li><a onclick="getCookbookInfo('${myCache.cookbookNames[i]}')">${myCache.cookbookNames[i]}</a></li>`;

  }
  cookbookNamesHTML += "</ul>";
  cookbookNamesHTML += `<button id="add-cookbook" onclick="displayAddCookbookForm()">Add Cookbook</button>`;
  var displayArea = document.getElementById('display-text');
  displayArea.innerHTML = cookbookNamesHTML;
}

//function to get cookbook info for selected cookbook

async function getCookbookInfo(cookbook_name) {
  console.log(`Trying to get cookbook info from 'localhost:50051' for ${cookbook_name}`);
  fetch(`http://localhost:50051/cookbook_info/${cookbook_name}`)
      .then(response => { return response.json() })
      .then(data => { 
            displayCookbookInfo(data, cookbook_name);
          })
      .catch((error) => { console.log(error) })
}

//function to display cookbook info in browser
function displayCookbookInfo(data, cookbook_name) {
  let cookbookInfoHTML = `<h3>${cookbook_name}</h3>`;
  cookbookInfoHTML += `<p>${data.message}</p>`;
  cookbookInfoHTML += `<p>Recipes: </p>`;
  cookbookInfoHTML += `<ul>`;
  for (let i = 0; i < data.recipes.length; i++) {
    cookbookInfoHTML += `<li><a onclick="getRecipeInfo('${data.recipes[i]}')">${data.recipes[i]}</a></li>`;
  }
  cookbookInfoHTML += `</ul>`;
  cookbookInfoHTML += `<button id="delete-cookbook" onclick="deleteCookbook('${cookbook_name}')">Delete Cookbook</button>`;
  var displayArea = document.getElementById('display-text');
  displayArea.innerHTML = cookbookInfoHTML;
}

//function to return to blank display data
function displayBlank() {
  var displayArea = document.getElementById('display-text');
  displayArea.innerHTML = "";  
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

//display a form to add a custom cookbook

function displayAddCookbookForm() {
  let formHTML = `<h3>Add a Cookbook</h3>`;
  formHTML += `<form id="add-cookbook-form">`;
  formHTML += `<label for="cookbook_name">Cookbook Name:</label><br>`;
  formHTML += `<input type="text" id="cookbook_name" name="cookbook_name">`;
  formHTML += `<br><label for="is_book">Is this a physical book?</label> <br>`;
  formHTML += `<input type="radio" id="is_book_yes" name="is_book" value="yes">`;
  formHTML += `<label for="is_book_yes">Yes</label>`;
  formHTML += `<input type="radio" id="is_book_no" name="is_book" value="no">`;
  formHTML += `<label for="is_book_no">No</label>`;
  formHTML += `<br><label for="website">Website:</label><br>`;
  formHTML += `<input type="text" id="website" name="website">`;
  formHTML += `<br><input type="submit" value="Add Cookbook">`;
  formHTML += `</form>`;

  let displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('add-cookbook-form').addEventListener('submit', handleAddCookbookSubmit);
}

//handle submit on add cookbook form

function handleAddCookbookSubmit(event) {
  event.preventDefault();
  let cookbook_name = document.getElementById('cookbook_name').value;
  let isBook = document.querySelector('input[name="is_book"]:checked').value === 'yes';
  let website = document.getElementById('website').value;
  addCookbook(cookbook_name, isBook, website);
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

//display a form to add a custom recipe

function displayAddRecipeForm() {
  let formHTML = `<h3>Add a Recipe</h3>`;
  formHTML += `<form id="add-recipe-form">`;
  formHTML += `<label for="recipe_name">Recipe Name:</label><br>`;
  formHTML += `<input type="text" id="recipe_name" name="recipe_name"><br>`;
  formHTML += `<br><label for="cookbook_name">Cookbook Name:</label><br>`;
  formHTML += `<select id="cookbook_name" name="cookbook_name">`;
  for(let i = 0; i < myCache.cookbookNames.length; i++) {
      formHTML += `<option value="${myCache.cookbookNames[i]}">${myCache.cookbookNames[i]}</option>`;
  }
  formHTML += `</select><br>`;
  formHTML += `<br><label for="servings">Number of Servings:</label><br>`;
  formHTML += `<select id="servings" name="servings">`;
  for(let i = 1; i <= 20; i++) {
      formHTML += `<option value="${i}">${i}</option>`;
  }
  formHTML += `</select><br>`;
  formHTML += `<br><input type="submit" value="Add Recipe">`;
  formHTML += `</form>`;

  let displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('add-recipe-form').addEventListener('submit', handleAddRecipeSubmit);
}

//handle submit on add cookbook form

function handleAddRecipeSubmit(event) {
  event.preventDefault();
  let recipe_name = document.getElementById('recipe_name').value;
  let cookbook_name = document.getElementById('cookbook_name').value;
  let servings = parseInt(document.getElementById('servings').value, 10)
  addRecipe(recipe_name, cookbook_name, servings);
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

//display a form to add a custom ingredient
function displayAddIngredientForm(recipe_name) {
  let formHTML = `<h3>Add an Ingredient to <span id="recipe-name">${recipe_name}</span></h3>`;
  formHTML += `<form id="add-ingredient-form">`;
  formHTML += `<label for="ingredient-name">Ingredient:</label><br>`;
  formHTML += `<input type="text" id="ingredient-name" name="ingredient-name"><br>`;
  formHTML += `<br><input type="submit" value="Add Ingredient">`;
  formHTML += `</form>`;

  let displayArea = document.getElementById('display-text');
  displayArea.innerHTML = formHTML;

  document.getElementById('add-ingredient-form').addEventListener('submit', handleAddIngredientSubmit);
}

//handle submit on add ingredient form

function handleAddIngredientSubmit(event) {
  event.preventDefault();
  let recipe_name = document.getElementById('recipe-name').innerText;
  let ingredient_name = document.getElementById('ingredient-name').value;
  addIngredient(recipe_name, ingredient_name);
}

//display ingredient name and a button to delete ingredient
function displayIngredient(ingredient_name) {
  let ingredientHTML = `<p>${ingredient_name}</p>`;
  ingredientHTML += `<button onclick="deleteIngredient('${ingredient_name}')">Delete Ingredient</button>`;

  let displayArea = document.getElementById('display-text');
  displayArea.innerHTML = ingredientHTML;
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