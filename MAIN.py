import pygame
import mysql.connector
from mysql.connector import errorcode
import sys
import random
import tempfile
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Music Window")


# Function to connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='somyaa',
            database='music_playlist'
        )
        if conn.is_connected():
            print("Connected to the database")
            return conn
        else:
            print("Failed to connect to the database")
            sys.exit(1)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied! Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: The specified database does not exist.")
        elif err.errno == errorcode.CR_CONNECTION_ERROR:
            print("Error: Failed to connect to MySQL server. Make sure MySQL is running.")
        else:
            print("MySQL Error:", err)
        sys.exit(1)
    except Exception as e:
        print("Unexpected error:", e)
        sys.exit(1)


# Function for user login or signup
def main_3():
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
                login_status, user_id, is_admin = login(conn, email, password)
                if login_status:
                    if is_admin:
                        return login_status, user_id, True
                    else:
                        return login_status, user_id, False
            elif n == "2":
                username = raw_input("Enter your username: ")
                email = raw_input("Enter your email: ")
                password = raw_input("Enter your password: ")
                if signup(conn, username, email, password):
                    return True, None, False
            else:
                print("Invalid choice. Please enter 1 or 2.")
                
        conn.close()
    else:
        print("Failed to connect to the database.")
        sys.exit(1)


# Function for user login
def login(conn, email, password):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = %s AND Password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            print("Login successful!")
            return True, user[0], user[3]  # Returning user_id and is_admin
        else:
            print("Invalid email or password.")
            return False, None, False
    except mysql.connector.Error as err:
        print("Error logging in:", err)
        return False, None, False
    finally:
        cursor.close()


# Function for user signup
def signup(conn, username, email, password):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users WHERE Email = %s", (email,))
        count_email = cursor.fetchone()[0]
        if count_email > 0:
            print("Email already registered. Please use a different Email.")
            return False

        if "@" not in email:
            print("Please enter a valid Email address.")
            return False

        cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = %s", (username,))
        count_username = cursor.fetchone()[0]
        if count_username > 0:
            print("Username already exists. Please choose a different username.")
            return False

        cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (%s, %s, %s)",
                       (username, email, password))
        conn.commit()
        print("Signup successful!")
        return True
    except mysql.connector.Error as err:
        print("Error signing up:", err)
        return False
    finally:
        cursor.close()


import pygame
import mysql.connector
from mysql.connector import errorcode
import tempfile
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Window")

def retrieve_random_mp3s(num_tracks=20):
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='somyaa',
            database='music_playlist'
        )
        cursor = conn.cursor()

        # Retrieve random MP3 files from the database
        query = "SELECT Track FROM Tracks ORDER BY RAND() LIMIT %s"
        cursor.execute(query, (num_tracks,))
        results = cursor.fetchall()

        # Initialize Pygame
        pygame.init()

        # Create a temporary directory to store MP3 files
        temp_dir = tempfile.mkdtemp()
        temp_files = []

        for index, result in enumerate(results):
            mp3_data = result[0]

            # Save the MP3 file to a temporary location
            temp_file_path = os.path.join(temp_dir, "temp_song_{}.mp3".format(index))

            with open(temp_file_path, 'wb') as file:
                file.write(mp3_data)
            temp_files.append(temp_file_path)

            # Play the MP3 file using Pygame
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()

            # Wait for the music to finish playing before loading the next track
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

            print("MP3 file {}/{} retrieved and playing...".format(index+1, num_tracks))

        return temp_files

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied! Check your username and password.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Error: The specified database does not exist.")
        else:
            print("MySQL Error:", err)
    except Exception as e:
        print("Unexpected error:", e)
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Usage
# Retrieve 20 random tracks
temp_files = retrieve_random_mp3s(num_tracks=20)

# Clean up temporary files
for temp_file in temp_files:
    os.remove(temp_file)

# Quit Pygame
pygame.quit()


# Function to generate a playlist
def generate_playlist(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT TrackID FROM Tracks ORDER BY RAND() LIMIT 20")
        tracks = cursor.fetchall()
        
        # Extracting track IDs from the fetched data
        track_ids = [track[0] for track in tracks]
        
        # Calling retrieve_random_mp3s with track IDs
        temp_files = retrieve_random_mp3s(track_ids)
        save_playlist = raw_input("Do you want to save this playlist? (y/n): ")
        if save_playlist.lower() == 'y':
            save_playlist_to_db(user_id, track_ids)
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        cursor.close()
        conn.close()


# Function to create a custom playlist
def create_custom_playlist(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT TrackID, Track FROM Tracks")
        tracks = cursor.fetchall()
        
        for idx, track in enumerate(tracks):
            print("{}. {}".format(idx + 1, track[1]))

        selected_tracks = []
        for _ in range(20):
            track_idx = int(raw_input("Select a track number: ")) - 1
            selected_tracks.append(tracks[track_idx][0])  # Appending TrackID

        # Calling retrieve_random_mp3s with selected track IDs
        temp_files = retrieve_random_mp3s(selected_tracks)
        save_playlist = raw_input("Do you want to save this playlist? (y/n): ")
        if save_playlist.lower() == 'y':
            save_playlist_to_db(user_id, selected_tracks)
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        cursor.close()
        conn.close()



# Function for user support


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


def continue_or_exit():
    while True:
        choice = raw_input("Do you want to continue to MAIN SUPPORT MENU(yes/no)? ").lower()
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")



def exit_program():
    print("Exiting program. Goodbye!")
    quit()
    
def support_menu():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            while True:
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
                    break
                else:
                    print("Invalid choice. Please select a number from 1 to 8.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            conn.close()
    else:
        print("Failed to connect to the database.")


# Function for admin work
def admin_work():
    print("--------------------------------ADMIN MENU-----------------------------")
    print("1.  Ban User")
    print("2.  Unban User")
    print("3.  Delete User Data")
    print("4.  Edit User Data")
    print("5.  Insert New User Manually")
    print("6.  Access User Data")
    print("7.  View Bugs, Errors & Reports")
    print("8.  View and Respond to Tickets")
    print("9.  Upload MP3 File")
    print("10. Add Admin")
    print("11. Exit")
    print("------------------------------------------------------------------------")
    return raw_input("ENTER OPTIONS FROM 1 TO 11:")

def view_bugs_errors_reports(cursor):
    try:
        cursor.execute("SELECT * FROM BugError")
        bug_errors_reports = cursor.fetchall()
        if bug_errors_reports:
            print("Bugs, Errors & Reports:")
            for data in bug_errors_reports:
                data_str = ' | '.join(str(elem) for elem in data)
                print(data_str)
        else:
            print("No bugs, errors, or reports found.")
    except mysql.connector.Error as err:
        print("Error fetching bug errors and reports:", err)

def view_respond_tickets(cursor):
    try:
        cursor.execute("SELECT * FROM Ticket")
        tickets = cursor.fetchall()
        if tickets:
            print("Tickets:")
            for ticket in tickets:
                ticket_str = ' | '.join(str(elem) for elem in ticket)
                print(ticket_str)
        else:
            print("No tickets found.")

        while True:
            tick_id_input = raw_input("Enter Tick_id to select ticket or m.menu: ")
            if tick_id_input.lower() == 'm.menu':
                break

            try:
                tick_id = int(tick_id_input)
                admin_response = raw_input("Enter admin response: ")
                cursor.execute("UPDATE Ticket SET Admin_Response = %s WHERE Tick_id = %s", (admin_response, tick_id))
                print("Admin response added successfully.")
                choice = raw_input("Do you want to respond to another ticket? (yes/no): ").lower()
                if choice == "no":
                    break
            except ValueError:
                print("Invalid input. Please enter a valid Tick_id.")
            except mysql.connector.Error as err:
                print("Error responding to ticket:", err)
    except mysql.connector.Error as err:
        print("Error fetching tickets:", err)

def validate_password():
    attempts_left = 5
    invalid_password_count = 0

    while attempts_left > 0:
        password_input = raw_input("ENTER ADMINISTRATOR PASSWORD: ")
        if password_input == 'somyaa':
            print("Login successful!")
            return True
        else:
            invalid_password_count += 1
            attempts_left -= 1
            print("SORRY WRONG PASSWORD [{} Attempts Left] :')".format(attempts_left))

    print("You've exhausted all login attempts. Please try again later.")
    return False

def ban_user(cursor):
    while True:
        user_input = raw_input("Enter UserID to ban or m.menu : ")

        if user_input.lower() == 'm.menu':
            break

        try:
            user_id = int(user_input)
            cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                cursor.execute("INSERT INTO Banned_Users (UserID, Username, Email, Password) VALUES (%s, %s, %s, %s)", user_data)
                cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))
                print("User banned successfully.")
                choice = raw_input("Do you want to ban another user? (yes/no): ").lower()
                if choice == "no":
                    break
            else:
                print("User with UserID {} does not exist.".format(user_id))
        except ValueError:
            print("Invalid input. Please enter a valid UserID.")
        except mysql.connector.Error as err:
            print("Error banning user:", err)

def unban_user(cursor):
    while True:
        user_input = raw_input("Enter UserID to unban or m.menu : ")

        if user_input.lower() == 'm.menu':
            break

        try:
            user_id = int(user_input)
            cursor.execute("SELECT * FROM Banned_Users WHERE UserID = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                cursor.execute("INSERT INTO Users (UserID, Username, Email, Password) VALUES (%s, %s, %s, %s)", user_data)
                cursor.execute("DELETE FROM Banned_Users WHERE UserID = %s", (user_id,))
                print("User unbanned successfully.")
                choice = raw_input("Do you want to unban another user? (yes/no): ").lower()
                if choice == "no":
                    break
            else:
                print("User with UserID {} is not banned.".format(user_id))
        except ValueError:
            print("Invalid input. Please enter a valid UserID.")
        except mysql.connector.Error as err:
            print("Error unbanning user:", err)

def delete_user_data(cursor):
    while True:
        user_input = raw_input("Enter UserID to delete data or m.menu : ")

        if user_input.lower() == 'm.menu':
            break

        try:
            user_id = int(user_input)
            cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))
                print("User data deleted successfully.")
                choice = raw_input("Do you want to delete data of another user? (yes/no): ").lower()
                if choice == "no":
                    break
            else:
                print("User with UserID {} does not exist.".format(user_id))
        except ValueError:
            print("Invalid input. Please enter a valid UserID.")
        except mysql.connector.Error as err:
            print("Error deleting user data:", err)

def edit_user_data(cursor):
    while True:
        user_input = raw_input("Enter UserID to edit data or m.menu : ")

        if user_input.lower() == 'm.menu':
            break

        try:
            user_id = int(user_input)
            cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                print("Current User Data:")
                print("UserID: {}, Username: {}, Email: {}, Password: {}".format(*user_data))
                new_username = raw_input("Enter new username: ")
                new_email = raw_input("Enter new email: ")
                new_password = raw_input("Enter new password: ")
                cursor.execute("UPDATE Users SET Username = %s, Email = %s, Password = %s WHERE UserID = %s",
                               (new_username, new_email, new_password, user_id))
                print("User data updated successfully.")
                choice = raw_input("Do you want to edit data of another user? (yes/no): ").lower()
                if choice == "no":
                    break
            else:
                print("User with UserID {} does not exist.".format(user_id))
        except ValueError:
            print("Invalid input. Please enter a valid UserID.")
        except mysql.connector.Error as err:
            print("Error editing user data:", err)

def insert_new_user(cursor):
    while True:
        username = raw_input("Enter new username: ")
        email = raw_input("Enter new email: ")
        password = raw_input("Enter new password: ")

        try:
            cursor.execute("SELECT COUNT(*) FROM Users WHERE Email = %s", (email,))
            count_email = cursor.fetchone()[0]
            if count_email > 0:
                print("Email already registered. Please use a different Email.")
                continue

            if "@" not in email:
                print("Please enter a valid Email address.")
                continue

            cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = %s", (username,))
            count_username = cursor.fetchone()[0]
            if count_username > 0:
                print("Username already exists. Please choose a different username.")
                continue

            cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (%s, %s, %s)",
                           (username, email, password))
            print("User inserted successfully.")
            choice = raw_input("Do you want to insert another user? (yes/no): ").lower()
            if choice == "no":
                break
        except mysql.connector.Error as err:
            print("Error inserting new user:", err)

def access_user_data(cursor):
    while True:
        user_input = raw_input("Enter UserID to access data or m.menu : ")

        if user_input.lower() == 'm.menu':
            break

        try:
            user_id = int(user_input)
            cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                print("User Data:")
                print("UserID: {}, Username: {}, Email: {}, Password: {}".format(*user_data))
            else:
                print("User with UserID {} does not exist.".format(user_id))
        except ValueError:
            print("Invalid input. Please enter a valid UserID.")
        except mysql.connector.Error as err:
            print("Error accessing user data:", err)


def admin_menu(cursor):
    while True:
        option = admin_work()
        if option == '1':
            ban_user(cursor)
        elif option == '2':
            unban_user(cursor)
        elif option == '3':
            delete_user_data(cursor)
        elif option == '4':
            edit_user_data(cursor)
        elif option == '5':
            insert_new_user(cursor)
        elif option == '6':
            access_user_data(cursor)
        elif option == '7':
            view_bugs_errors_reports(cursor)
        elif option == '8':
            view_respond_tickets(cursor)
        elif option == '9':
            print("UPLOADING MP3 FILES IS CURRENTLY DISABLED.")
        elif option == '10':
            print("ADDING NEW ADMINISTRATOR IS CURRENTLY DISABLED.")
        elif option == '11':
            break
        else:
            print("Invalid option. Please select a number from 1 to 11.")



# Function to handle user options
def user_options(user_id):
    while True:
        conn = connect_to_database()
        print("------------------------NAPSTER0z------------------------")
        print("1. Generate a Playlist")
        print("2. Create a Custom Playlist")
        print("3. Support")
        print("4. Exit")
        print("---------------------------------------------------------")
        option = raw_input("Choose option: ")

        if option == "1":
            generate_playlist(user_id)
        elif option == "2":
            create_custom_playlist(user_id)
        elif option == "3":
            support_menu()
        elif option == "4":
            break
        else:
            print("Invalid option. Please try again.")



    conn.commit
    conn.close() 


# Main program
def main():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        while True:
            login_successful, user_id, is_admin = main_3()

            if login_successful:
                cursor.execute("SELECT * FROM Admin WHERE UserID = %s", (user_id,))
                if cursor.fetchone():
                    print("1.Admin Work")
                    print("2.Continue As A Normal User")
                    n=raw_input("Enter 1 or 2:")
                    if n == "1":
                        main_1()  # Calling admin work

                    elif n == "2":
                        user_options(user_id)

                    
                    else:
                        print "ENTER A VALID OPTION"

                else:
                    user_options(user_id)
                        
                        
                    
                
            else:
                print("Login/Signup unsuccessful. Please try again.")


        conn.commit

        cursor.close()  # Close the cursor
        conn.close()    # Close the connection
    else:
        print("Failed to connect to the database.")
        sys.exit(1)




if __name__ == "__main__":
    main()
