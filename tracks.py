import mysql.connector
from mysql.connector import errorcode

def create_tracks_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tracks (
                TrackID INT AUTO_INCREMENT PRIMARY KEY,
                Track_Title VARCHAR(255) NOT NULL,
                Artist_NAME VARCHAR(255),
                Track MEDIUMBLOB
            )
        """)
        print("Tracks table created successfully!")
    except mysql.connector.Error as err:
        print("Error creating Tracks table:", err)

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="somyaa",
            database="music_playlist"
        )
        if conn.is_connected():
            print("Connected to the database successfully!")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Error:", err)
        return None

def main():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            create_tracks_table(cursor)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error during the operation:", err)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()
