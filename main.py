from dotenv import load_dotenv
import os
import requests
from database import *
#Documentation for API
#https://developer.edamam.com/edamam-docs-recipe-api-v1


#Load environment variables from .env file
load_dotenv()

#Get app id from environment variables
app_id = os.getenv("APP_ID")

#Get api key from environment variables
api_key = os.getenv("API_KEY")

#Create/user username to save favorite recipes
allUsers = get_all_users()
User = input("What is your username: ")

if User not in [user[1] for user in allUsers]:
    add_user(User)

#Get user id
user_id = get_user_id_by_username(User)

#Decide between favorite recipe or new one
if User in [user[1] for user in allUsers]:
    userChoice = input("Would you like to view favorite recipes or would you like to find a new one (1. favorite 2. new): ")

    if userChoice == '1':
        # Make sure user has favorite recipes
        favorite_recipes = get_user_recipes(user_id)
        if not favorite_recipes:
            print("You have no favorite recipes.")
        else:
            print(f"Your favorite recipes: {favorite_recipes}")
        userChoice = input("Would you like to find a new recipe (y/n): ")
        if userChoice.lower() != 'y':
            exit()

#Ask user what they are looking for in a recipe
foodChoice = input("Enter what food you want a recipe for: ")
proteinAmount = input("Enter how much protein do you need (Ex: 30): ")
calorieChoice = input("Enter the range of calories you want (Ex: 300-400): ")

#Calls api
response = requests.get(f"https://api.edamam.com/search?app_id={app_id}&app_key={api_key}&q={foodChoice}&nutrients[PROCNT]={proteinAmount}&calories={calorieChoice}", timeout=5)
data = response.json()

#Create recipe object for each recipe
class Recipes:
    def __init__(self, recipe_num, recipe_name, ingredients, instructions, calories, protein, carbohydrates, fat, vitamins, minerals):
        self.recipe_number = recipe_num
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.instructions = instructions
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fat = fat
        self.vitamins = vitamins
        self.minerals = minerals


#Extract individual information about nutrients
def extract_nutritional_info(recipe_data):
    nutrients = recipe_data.get('totalNutrients', {})
    
    #Extract the specific nutrients you need
    protein = nutrients.get('PROCNT', {}).get('quantity', 0)
    carbohydrates = nutrients.get('CHOCDF', {}).get('quantity', 0)
    fat = nutrients.get('FAT', {}).get('quantity', 0)
    vitamins = {}
    minerals = {}
    for key, nutrient_data in nutrients.items():
        if 'VITA' in key or 'VITB' in key or 'VITC' in key:
            vitamins[key] = nutrient_data.get('quantity', 0)
        elif 'CA' in key or 'FE' in key or 'MG' in key:
            minerals[key] = nutrient_data.get('quantity', 0)

    return protein, carbohydrates, fat, calories, vitamins, minerals





#Create an array to store recipe objects
recipes_list = []

#Function to display and add recipe to favorites
def display_and_add_to_favorites(user_id, recipes_list):
    for idx, recipe in enumerate(recipes_list):
        print(f"Recipe Number {idx + 1}:")
        print("Recipe Name:", recipe.recipe_name)
        print("Instructions:", recipe.instructions)
        print("Calories:", recipe.calories)
        print("Ingredients:")
        for ingredient in recipe.ingredients:
            print("- " + ingredient)
        print("Nutritional Information:")
        print(f"Protein: {protein:.2f} grams")
        print(f"Carbohydrates: {carbohydrates:.2f} grams")
        print(f"Fat: {fat:.2f} grams")
        print(f"Calories: {calories}")
        print("Vitamins:", ', '.join([f"{nutrient}: {value:.2f}" for nutrient, value in vitamins.items()]))
        print("Minerals:", ', '.join([f"{nutrient}: {value:.2f}" for nutrient, value in minerals.items()]))
        print("\n\n\n")
    while True:
        num = int(input("Enter the number of the recipe you want to favorite (or 0 to exit): "))
        if num == 0:
            break
        elif 1 <= num <= len(recipes_list):
            #Convert the list of ingredients to a string, separated by newlines
            ingredients_str = '\n'.join(recipe.ingredients)

            recipe = recipes_list[num - 1]
            add_to_favorite_recipes(user_id, recipe.recipe_name, ingredients_str, recipe.instructions, recipe.calories, recipe.protein, recipe.carbohydrates, recipe.fat, recipe.vitamins, recipe.minerals)
            print(f"Recipe {num} has been added to your favorites.")
        else:
            print("Invalid recipe number. Please enter a valid recipe number or 0 to exit.")







#Loop through the recipes
currentRecipe = 0
for recipe_data in data.get('hits', []):
    recipe = recipe_data.get('recipe')
    label = recipe['label']
    image = recipe['image']
    source = recipe['source']
    url = recipe['url']
    calories = recipe['calories']
    ingredients = recipe['ingredientLines']

    #Extract nutritional information
    nutrients = recipe['totalNutrients']

    #Extract specific nutritional information using function
    protein, carbohydrates, fat, calories, vitamins, minerals = extract_nutritional_info(recipe)

    #Display recipe details
    print("Recipe Name:", label)
    print("Image URL:", image)
    print("Source:", source)
    print("URL:", url + '\n\n')
    print("Calories:", calories)
    print("Ingredients:")
    for ingredient in ingredients:
        print("- " + ingredient)

    #Display nutritional information
    print("\nNutritional Information:")
    for nutrient_name, nutrient_data in nutrients.items():
        nutrient_label = nutrient_data['label']
        nutrient_quantity = nutrient_data['quantity']
        nutrient_unit = nutrient_data['unit']
        print(f"- {nutrient_label}: {nutrient_quantity:.2f} {nutrient_unit}")


    #Create a recipe object and add it to the list
    recipe_obj = Recipes(currentRecipe, label, ingredients, url, calories, protein, carbohydrates, fat, vitamins, minerals)
    recipes_list.append(recipe_obj)
    currentRecipe += 1
        



#Add to favorite recipes
userChoice = input("Would you like to add a recipe to favorites? (y/n): ")
if userChoice == 'y':
    display_and_add_to_favorites(user_id, recipes_list)

elif userChoice == 'n':
    exit()

else:
    print("Invalid choice.")

