from dotenv import load_dotenv
import os
import mysql.connector
#from main import User

#user = User()
#user.name = "test2"
#user.favoriteRecipes = 

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

def addValues(user):
    sql = "INSERT INTO users (username, favoriteRecipes[]) VALUES (%s, %s)"
    val = ("user.name", "user.favoriteRecipes")
    mycursor.execute(sql, val)


def showValues():
    mycursor.execute("SELECT * FROM users")
    for x in mycursor:
        print(x)

