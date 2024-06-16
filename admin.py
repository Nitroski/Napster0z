import mysql.connector
from getpass import getpass

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="somyaa",
            database="music_playlist"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

def create_admin_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Admin (
                AdminID INT AUTO_INCREMENT PRIMARY KEY,
                UserID INT,
                Password VARCHAR(255)
            )
        """)
        conn.commit()
        print("Admin table created successfully!")
    except mysql.connector.Error as err:
        print("Error creating Admin table:", err)
    finally:
        if 'cursor' in locals():
            cursor.close()

def add_admin_user(conn, user_id, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Admin (UserID, Password) VALUES (%s, %s)", (user_id, password))
        conn.commit()
        print("User added to Admin table successfully!")
        return True
    except mysql.connector.Error as err:
        print("Error adding user to Admin table:", err)
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()

def main():
    conn = connect_to_database()
    if conn:
        create_admin_table(conn)
        user_id = input("Enter UserID: ")
        password = getpass("Enter Password: ")
        if user_id.isdigit():
            if add_admin_user(conn, int(user_id), password):
                print("User added to Admin table successfully!")
            else:
                print("Failed to add user to Admin table.")
        else:
            print("Invalid UserID. Please enter a valid integer.")
        conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
