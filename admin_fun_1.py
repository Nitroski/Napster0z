import mysql.connector

def connect_to_database():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="somyaa",
            database="music_playlist"
        )
        return con
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

def menu():
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
##    print("10. Insert Genre")
##    print("11. Insert Artist")
    print("10. Add Admin")
    print("11. Exit")
    print("------------------------------------------------------------------------")
    return raw_input("ENTER OPTIONS FROM 1 TO 13:")

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
                choice = raw_input("Do you want to BAN another user? (yes/no): ").lower()
                if choice == "no":
                    return
            else:
                print("User not found.")
        except ValueError:
            print("Invalid input. Please enter a valid UserID.")
        except mysql.connector.Error as err:
            print("Error banning user:", err)

def unban_user(cursor):
    try:
        cursor.execute("SELECT * FROM Banned_Users")
        banned_users = cursor.fetchall()
        if banned_users:
            print("Banned Users:")
            for user in banned_users:
                user_str = ' | '.join(str(elem) for elem in user)
                print(user_str)
        else:
            print("No banned users.")

        while True:
            user_input = raw_input("Enter UserID to Unban or m.menu: ")
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
                    choice = raw_input("Do you want to UNBAN another user? (yes/no): ").lower()
                    if choice == "no":
                        return
                else:
                    print("User not found.")
            except ValueError:
                print("Invalid input. Please enter a valid UserID.")
            except mysql.connector.Error as err:
                print("Error unbanning user:", err)
    except mysql.connector.Error as err:
        print("Error fetching banned users:", err)

def delete_user(cursor):
    try:
        while True:
            user_id_input = raw_input("Enter UserID to delete or m.menu: ")
            if user_id_input.lower() == 'm.menu':
                break

            try:
                user_id = int(user_id_input)
                cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))
                print("User deleted successfully.")
                choice = raw_input("Do you want to DELETE another user? (yes/no): ").lower()
                if choice == "no":
                    break
            except ValueError:
                print("Invalid input. Please enter a valid UserID.")
            except mysql.connector.Error as err:
                print("Error deleting user:", err)
    except mysql.connector.Error as err:
        print("Error deleting user:", err)

def edit_user(cursor):
    try:
        while True:
            user_id_input = raw_input("Enter UserID to edit or m.menu: ")
            if user_id_input.lower() == 'm.menu':
                break

            try:
                user_id = int(user_id_input)
                new_username = raw_input("Enter new username: ")
                new_email = raw_input("Enter new email: ")
                new_password = raw_input("Enter new password: ")
                cursor.execute("UPDATE Users SET Username = %s, Email = %s, Password = %s WHERE UserID = %s",

                (new_username, new_email, new_password, user_id))
                print("User data updated successfully.")
                choice = raw_input("Do you want to EDIT another user? (yes/no): ").lower()
                if choice == "no":
                    break
            except ValueError:
                print("Invalid input. Please enter a valid UserID.")
            except mysql.connector.Error as err:
                print("Error editing user data:", err)
    except mysql.connector.Error as err:
        print("Error editing user data:", err)

def add_admin(conn, admin_id, user_id, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Admin (AdminID, UserID, Password) VALUES (%s, %s, %s)", (admin_id, user_id, password))
        conn.commit()
        print("User added to Admin table successfully!")
        return True
    except mysql.connector.Error as err:
        print("Error adding user to Admin table:", err)
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()

def add_user(conn, user_id, password, is_admin=False):
    try:
        cursor = conn.cursor()
        if is_admin:
            cursor.execute("INSERT INTO Admin (UserID, Password) VALUES (%s, %s)", (user_id, password))
        else:
            cursor.execute("INSERT INTO Users (UserID, Password) VALUES (%s, %s)", (user_id, password))
        conn.commit()
        print("User added successfully!")
        return True
    except mysql.connector.Error as err:
        print("Error adding user:", err)
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()

def see_all_users(cursor):
    try:
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        if users:
            for user in users:
                user_str = ' | '.join(str(elem) for elem in user)
                print(user_str)
        else:
            print("No users found.")
    except mysql.connector.Error as err:
        print("Error fetching users:", err)

def upload_mp3(cursor, file_path, title, artist):
    try:
        with open(file_path, 'rb') as file:
            mp3_data = file.read()

        query = "INSERT INTO Tracks (Track_Title, Artist_NAME, Track) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, artist, mp3_data))

        print("MP3 uploaded successfully!")

    except Exception as e:
        print("Error: %s" % e)

def upload_mp3_prompt(cursor):
    file_path = raw_input("Enter the file path of the MP3: ").strip('"')
    title = raw_input("Enter the title of the MP3: ")
    artist = raw_input("Enter the artist of the MP3: ")
    upload_mp3(cursor, file_path, title, artist)

##def insert_genre(cursor):
##    try:
##        genre_name = raw_input("Enter Genre Name: ")
##        cursor.execute("INSERT INTO Genres (GenreName) VALUES (%s)", (genre_name,))
##        print("Genre inserted successfully!")
##    except mysql.connector.Error as err:
##        print("Error:", err)
##
##def insert_artist(cursor):
##    try:
##        artist_name = raw_input("Enter Artist Name: ")
##        cursor.execute("INSERT INTO Artists (ArtistName) VALUES (%s)", (artist_name,))
##        print("Artist inserted successfully!")
##    except mysql.connector.Error as err:
##        print("Error:", err)

def main():
    if validate_password():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            while True:
                choice = menu()
                if choice == "1":
                    ban_user(cursor)
                elif choice == "2":
                    unban_user(cursor)
                elif choice == "3":
                    delete_user(cursor)
                elif choice == "4":
                    edit_user(cursor)
                elif choice == "5":
                    add_user(conn, user_id, password)
                elif choice == "6":
                    see_all_users(cursor)
                elif choice == "7":
                    view_bugs_errors_reports(cursor)
                elif choice == "8":
                    view_respond_tickets(cursor)
                elif choice == "9":
                    upload_mp3_prompt(cursor)
##                elif choice == "10":
##                    insert_genre(cursor)
##                elif choice == "11":
##                    insert_artist(cursor)
                elif choice == "10":
                    add_admin(conn, admin_id, user_id, password)
                elif choice == "11":
                    print("Exiting...")
                    break
                else:
                    print("Invalid Option!")
            cursor.close()
            conn.close()
    else:
        print("Incorrect password!")

if __name__ == "__main__":
    main()
