import mysql.connector
import random

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

def forgot_password(cursor, conn):
    username = raw_input("Enter your username: ")
    email = raw_input("Enter your email: ")
    new_password = raw_input("Enter your new password: ")
    
    cursor.execute("SELECT * FROM Users WHERE Username = %s AND Email = %s", (username, email))
    user_data = cursor.fetchone()
    if user_data:
        try:
            cursor.execute("UPDATE Users SET Password = %s WHERE Username = %s AND Email = %s", (new_password, username, email))
            print("Password updated successfully!")
            conn.commit()  # Committing changes using the connection object
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
    else:
        print("Invalid username or email.")

    if continue_or_exit():
        return True
    else:
        return False

def change_username(cursor, conn):
    while True:
        username = raw_input("Enter your username: ")
        email = raw_input("Enter your email: ")
        password = raw_input("Enter your password: ")
        new_username = raw_input("Enter your new username: ")

        cursor.execute("SELECT * FROM Users WHERE Username = %s", (new_username,))
        existing_username = cursor.fetchone()

        if existing_username:
            print("Username already exists. Please choose a different one.")
        else:
            cursor.execute("SELECT * FROM Users WHERE Username = %s AND Email = %s AND Password = %s", (username, email, password))
            user_data = cursor.fetchone()
            if user_data:
                try:
                    cursor.execute("UPDATE Users SET Username = %s WHERE Username = %s AND Email = %s AND Password = %s", (new_username, username, email, password))
                    print("Username updated successfully!")
                    conn.commit()  
                    break  
                except mysql.connector.Error as err:
                    print("MySQL Error:", err)
                    break  
            else:
                print("Invalid username, email, or password.")
                break  

    if continue_or_exit():
        return True
    else:
        return False

def change_email(cursor, conn):
    while True:
        username = raw_input("Enter your username: ")
        email = raw_input("Enter your email: ")
        password = raw_input("Enter your password: ")
        new_email = raw_input("Enter your new email: ")

        cursor.execute("SELECT * FROM Users WHERE Email = %s", (new_email,))
        existing_email = cursor.fetchone()

        if existing_email:
            print("Email already exists. Please choose a different one.")
        else:
            cursor.execute("SELECT * FROM Users WHERE Username = %s AND Email = %s AND Password = %s", (username, email, password))
            user_data = cursor.fetchone()
            if user_data:
                try:
                    cursor.execute("UPDATE Users SET Email = %s WHERE Username = %s AND Email = %s AND Password = %s", (new_email, username, email, password))
                    print("Email updated successfully!")
                    conn.commit() 
                    break  
                except mysql.connector.Error as err:
                    print("MySQL Error:", err)
                    break 
            else:
                print("Invalid username, email, or password.")
                break  

    if continue_or_exit():
        return True
    else:
        return False

def report_bug(cursor, conn):
    user_response = raw_input("Describe the bug/error: ")
    try:
        cursor.execute("INSERT INTO BugError (Summary) VALUES (%s)", (user_response,))
        print("THANKS FOR BRINGING THIS INFO IN FRONT OF US :)")
        print("OUR TEAM WILL BE FIXING IT SOON :3")
        print("PEOPLE LIKE YOU MAKE THIS PLATFORM BETTER >..<")
        conn.commit()  # Committing changes using the connection object
    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    if continue_or_exit():
        return True
    else:
        return False

def open_ticket(cursor, conn):
    username = raw_input("Enter your username: ")
    user_response = raw_input("Describe your issue: ")
    tick_id = random.randint(10000000, 99999999)
    try:
        cursor.execute("INSERT INTO Ticket (Tick_id, Username, Summary) VALUES (%s, %s, %s)", (tick_id, username, user_response))
        print("TICKET ID:", tick_id)
        print("OUR TEAM WILL SHORTLY REACH OUT TO YOU, DON'T WORRY :)")
        conn.commit()  # Committing changes using the connection object
    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    if continue_or_exit():
        return True
    else:
        return False

def follow_up_ticket(cursor, conn):
    username = raw_input("Enter your username: ")
    ticket_id = raw_input("Enter your ticket ID: ")
    try:
        cursor.execute("SELECT Admin_Response FROM Ticket WHERE Username = %s AND Tick_id = %s", (username, ticket_id))
        result = cursor.fetchone()
        if result:
            print("Admin Response:",result[0].encode('ascii'))
        else:
            print("Invalid ticket ID or username.")
    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    if continue_or_exit():
        return True
    else:
        return False

def contact_info():
    print("IT SAID CONTACT: xyz@gmail.com")
    print("JUST EMAIL US YOUR CONCERNS OUR TEAM WILL RESPOND TO YOUR 'QURIES' ")
    print("NOW GO ON EXIT YOU CUTE BUFFOON :3")

def exit_program():
    print("Exiting program. Goodbye!")
    quit()

def main_menu():
    print("---------------------SUPPORT---------------------")
    print("1. Forgot Password & Change it")
    print("2. Change User Name")
    print("3. Change EMail")
    print("4. Report a Bug/Error")
    print("5. OPEN A TICKET")
    print("6. Follow up on TICKET")
    print("7. ANYTHING ELSE (CONTACT: napster0z@gmail.com)")
    print("8. Exit")
    print("-------------------------------------------------")

def continue_or_exit():
    while True:
        choice = raw_input("Do you want to continue to MAIN SUPPORT MENU(yes/no)? ").lower()
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

def main():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            while True:
                main_menu()
                n = raw_input("Enter your choice (1-8): ")

                if n == "1":
                    if not forgot_password(cursor, conn):
                        break
                elif n == "2":
                    if not change_username(cursor, conn):
                        break
                elif n == "3":
                    if not change_email(cursor, conn):
                        break
                elif n == "4":
                    if not report_bug(cursor, conn):
                        break
                elif n == "5":
                    if not open_ticket(cursor, conn):
                        break
                elif n == "6":
                    if not follow_up_ticket(cursor, conn):
                        break
                elif n == "7":
                    contact_info()
                    if not continue_or_exit():
                        break
                elif n == "8":
                    exit_program()
                else:
                    print("Invalid choice. Please select a number from 1 to 8.")

            cursor.close()  # Closing cursor
            conn.close()  # Closing connection

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            conn.close()
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()
