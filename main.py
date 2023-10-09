from dotenv import load_dotenv
import os
import requests
from database import *
#Documentation for API
#https://developer.edamam.com/edamam-docs-recipe-api-v1


# Load environment variables from .env file
load_dotenv()

# Get app id from environment variables
app_id = os.getenv("APP_ID")

# Get api key from environment variables
api_key = os.getenv("API_KEY")

# Create/user username to save favorite recipes
allUsers = get_all_users()
User = input("What is your username: ")

if User not in [user[1] for user in allUsers]:
    add_user(User)

# Get user id
user_id = get_user_id_by_username(User)

# Decide between favorite recipe or new one
if User in [user[1] for user in allUsers]:
    userChoice = input("Would you like to view favorite recipes or would you like to find a new one (1. favorite 2. new): ")

    if userChoice == '1':
        # Make sure user has favorite recipes
        favorite_recipes = get_user_recipes(user_id)
        if not favorite_recipes:
            print("You have no favorite recipes.")
        else:
            print(f"Your favorite recipes: {favorite_recipes}")
        userChoice = input("Would you like to find a new recipe: (y/n)")
        if userChoice.lower() != 'y':
            exit()

# Ask user what they are looking for in a recipe
foodChoice = input("Enter what food you want a recipe for: ")
proteinAmount = input("Enter how much protein you need: ")
calorieChoice = input("Enter the range of calories you want (Ex: 300-400): ")

response = requests.get(f"https://api.edamam.com/search?app_id={app_id}&app_key={api_key}&q={foodChoice}&nutrients[PROCNT]={proteinAmount}&calories={calorieChoice}")
data = response.json()

#Create recipe object for each recipe

class Recipes:
    def __init__(self, recipe_name, ingredients, instructions, calories, protein, carbohydrates, fat, vitamins, minerals):
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.instructions = instructions
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fat = fat
        self.vitamins = vitamins
        self.minerals = minerals

# Extract recipe details
currentRecipe = 0
try:
    while currentRecipe <= data['count']:
        recipe = data['hits'][currentRecipe]['recipe']
        label = recipe['label']
        image = recipe['image']
        source = recipe['source']
        url = recipe['url']
        calories = recipe['calories']
        ingredients = recipe['ingredientLines']

        # Display recipe details
        print(f"\n\nRecipe Number {currentRecipe}")
        print("Recipe Name:", label)
        print("Image URL:", image)
        print("Source:", source)
        print("URL:", url + '\n\n')
        print("Calories:", calories)
        print("Ingredients:")
        for ingredient in ingredients:
            print("- " + ingredient)

        # Extract nutritional information
        nutrients = recipe['totalNutrients']

        # Display nutritional information
        print("\nNutritional Information:")
        for nutrient_name, nutrient_data in nutrients.items():
            nutrient_label = nutrient_data['label']
            nutrient_quantity = nutrient_data['quantity']
            nutrient_unit = nutrient_data['unit']
            print(f"- {nutrient_label}: {nutrient_quantity:.2f} {nutrient_unit}")
        recipe += str(currentRecipe)
        recipe = Recipes(label, ingredients, url, calories, )
        currentRecipe += 1

except IndexError:
    print("")
        



# Add to favorite recipes
userChoice = input("Would you like to add a recipe to favorites? (y/n)")
if userChoice == 'y':
    userChoice = input("Enter the number for the recipe you want to favorite: ")
    add_to_favorite_recipes()

elif userChoice == 'n':
    exit()

else:
    print("Invalid choice.")

