import mysql.connector

def create_playlists_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Playlists (
                PlaylistID INT AUTO_INCREMENT PRIMARY KEY,
                UserID INT,
                PlaylistName VARCHAR(100) NOT NULL,
                Genre VARCHAR(50) NOT NULL,
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )
        """)
        print("Playlists Table created successfully!")
    except mysql.connector.Error as err:
        print("Error creating Playlists table:", err)

# Establishing connection to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="somyaa",
    database="music_playlist"
)


print("CONNECTION STATUS:", conn.is_connected())


cursor = conn.cursor()

create_playlists_table(cursor)


conn.commit()
cursor.close()
conn.close()
