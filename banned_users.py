import mysql.connector

def create_banned_users_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Banned_Users (
                UserID INT PRIMARY KEY,
                Username VARCHAR(50) NOT NULL,
                Email VARCHAR(100) NOT NULL,
                Password VARCHAR(100) NOT NULL)""")
        print("Banned_Users Table created successfully!")
    except mysql.connector.Error as err:
        print("Error creating Banned_Users table:", err)

c = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="somyaa",
    database="music_playlist"
)

print("CONNECTION STATUS:", c.is_connected())

x = c.cursor()

create_banned_users_table(x)

c.commit()
c.close()
