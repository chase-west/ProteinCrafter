from dotenv import load_dotenv
import os
import mysql.connector



# Load environment variables from .env file
load_dotenv()

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = os.getenv("SQL_PW"),
    database = "SavedRecipes",
    port="3306"
    )

mycursor = mydb.cursor()
mycursor.execute("USE SavedRecipes")

def get_all_users():
    sql = "SELECT * FROM Users"
    mycursor.execute(sql)
    all_users = mycursor.fetchall()
    return all_users


def get_user_id_by_username(username):
    sql = "SELECT user_id FROM Users WHERE username = %s"
    mycursor.execute(sql, (username,))
    result = mycursor.fetchone()
    if result:
        return result[0]  # Return the user_id
    else:
        return None  # User not found


def add_to_favorite_recipes(user_id, recipe_name, ingredients, instructions, calories, protein, carbohydrates, fat, vitamins, minerals):
    sql = "INSERT INTO Recipes (user_id, recipe_name, ingredients, instructions, calories, protein, carbohydrates, fat, vitamins, minerals) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (user_id, recipe_name, ingredients, instructions, calories, protein, carbohydrates, fat, vitamins, minerals)
    mycursor.execute(sql, values)
    mydb.commit()

def get_user_recipes(user_id):
    sql = "SELECT * FROM Recipes WHERE user_id = %s"
    mycursor.execute(sql, (user_id,))
    user_recipes = mycursor.fetchall()
    return user_recipes

def add_user(username):
    sql = "INSERT INTO Users (username) VALUES (%s)"
    val = (username,)
    mycursor.execute(sql, val)
    mydb.commit()

def display_all():
    mycursor.execute("SELECT * FROM Users")
    users_result = mycursor.fetchall()
    
    mycursor.execute("SELECT * FROM Recipes")
    recipes_result = mycursor.fetchall()
    
    print("Users:")
    for user in users_result:
        print(user)
        
    print("\nRecipes:")
    for recipe in recipes_result:
        print(recipe)


create_users_table = """
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
)
"""

#mycursor.execute(create_users_table)

#instructions = url from api call 
create_recipes_table = """
CREATE TABLE Recipes (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    recipe_name VARCHAR(100) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    calories INT,
    protein DECIMAL(10, 2),
    carbohydrates DECIMAL(10, 2),
    fat DECIMAL(10, 2),
    vitamins TEXT,
    minerals TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
"""

display_all()

#mycursor.execute(create_recipes_table)




