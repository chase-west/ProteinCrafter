from dotenv import load_dotenv
import os
import requests
#Documentation for API
#https://developer.edamam.com/edamam-docs-recipe-api-v1


# Load environment variables from .env file
load_dotenv()

# Get app id from environment variables
app_id = os.getenv("APP_ID")

# Get api key from environment variables
api_key = os.getenv("API_KEY")


#Ask user what looking for in recipe
foodChoice = input("Enter what food you want a recipe for: ")
proteinAmount = input("Enter how much protein you need: ")
calorieChoice = input("Enter the range of calories you want (Ex: 300-400): ")


response = requests.get(f"https://api.edamam.com/search?app_id={app_id}&app_key={api_key}&q={foodChoice}&nutrients[PROCNT]={proteinAmount}&calories={calorieChoice}")

data = response.json()

#Create user class to send needed information to database
class User:
   def __init__(self, name, favoriteRecipes):
      self.name = name
      self.favoriteRecipes = favoriteRecipes

class FavoriteRecipeData:
    def __init__(self, recipe):
        self.calories = recipe['calories']
        self.ingredients = recipe['ingredientLines']
        self.recipeName = recipe['label']
      


# Extract recipe details
currentRecipe = 0
while currentRecipe != data['count']:
  recipe = data['hits'][currentRecipe]['recipe']
  label = recipe['label']
  image = recipe['image']
  source = recipe['source']
  url = recipe['url']
  calories = recipe['calories']
  ingredients = recipe['ingredientLines']
  


  # Display recipe details
  print("\n\nRecipe Label:", label)
  print("Image URL:", image)
  print("Source:", source)
  print("URL:", url)
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
  currentRecipe += 1

print(response.status_code)