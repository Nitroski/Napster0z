import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="somyaa",
            database="music_playlist")
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

def signup(conn, username, email, password):
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Users WHERE Email = %s", (email,))
        count_email = cursor.fetchone()[0]
        if count_email > 0:
            print("Email already registered. Please use a different Email.")
            return False

        # VALIDATING EMAIL
        #pip. FUNCTIONS NOT ISTALLING/WORKING
        #(FOR ATLEAST CHECKING DOMAIN AND OTP[OTP FOR BOTH EMAIL & PHONE NO])
        #IT SAYS COULDNT FIND FOR YOUR VERSION
        if "@" not in email:
            print("Please enter a valid Email address.")
            return False

        cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = %s", (username,))
        count_username = cursor.fetchone()[0]
        if count_username > 0:
            print("User Name already exists. Please choose a different username.")
            return False

        cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        print("Signup successful!")
        return True
    except mysql.connector.Error as err:
        print("Error signing up:", err)
        return False
    except Exception as e:
        print("An unexpected error occurred:", e)
        return False

def login(conn, email, password):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = %s AND Password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            print("Login successful!")
            return True
        else:
            print("Invalid email or password.")
            return False
    except mysql.connector.Error as err:
        print("Error logging in:", err)
        return False
    except Exception as e:
        print("An unexpected error occurred:", e)
        return False

def main():
    conn = connect_to_database()
    if conn:
        while True:
            print("-----------WELCOME TO NAPSTER0z-----------")
            print("1. Login")
            print("2. Signup")
            print("Enter 1 for login or 2 for signup")
            print("------------------------------------------")
            n = raw_input("Enter your choice: ")
            if n == "1":
                email = raw_input("Enter your email: ")
                password = raw_input("Enter your password: ")
                if login(conn, email, password):
                    break
            elif n == "2":
                username = raw_input("Enter your username: ")
                email = raw_input("Enter your email: ")
                password = raw_input("Enter your password: ")
                if signup(conn, username, email, password):
                    break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
