import mysql.connector
import random

def generate_ticket_id():
    return random.randint(10000000, 99999999)

def create_ticket_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ticket (
                Tick_id INT AUTO_INCREMENT PRIMARY KEY,
                UserID INT,
                Username VARCHAR(255)NOT NULL,
                Email VARCHAR(255)NOT NULL,
                Summary VARCHAR(1000)NOT NULL,
                Admin_Response VARCHAR(500),
                FOREIGN KEY (UserID) REFERENCES Users(UserID))""")
        print("Ticket Table created successfully!")
    except mysql.connector.Error as err:
        print("Error creating Ticket table:", err)


def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="somyaa",
            database="music_playlist"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

def main():
    
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('USE music_playlist;')
            
            create_ticket_table(cursor)
            
            
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()

    
