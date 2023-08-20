import requests

#Get app id from text file
file = open("app_id.txt", "r")
app_id = file.read() 

#Get api key from text file
file = open("api_key.txt", "r")
api_key = file.read() 

#Ask user what looking for in recipe
foodChoice = input("Enter what food you want a recipe for: ")
proteinAmount = input("Enter how much protein you need: ")
calorieChoice = input("Enter the range of calories you want (Ex: 300-400): ")


response = requests.get(f"https://api.edamam.com/search?app_id={app_id}&app_key={api_key}&q={foodChoice}&nutrients[PROCNT]={proteinAmount}&calories={calorieChoice}")

data = response.json()

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