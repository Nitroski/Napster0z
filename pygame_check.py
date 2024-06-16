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
    temp_files = []
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

        # Create a temporary directory to store MP3 files
        temp_dir = tempfile.mkdtemp()

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
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied! Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
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
            print("Database connection closed.")

        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
                print("Temporary file {} removed.".format(temp_file))
            except Exception as e:
                print("Error removing temporary file:", e)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Usage
# Retrieve 20 random tracks
temp_files = retrieve_random_mp3s(num_tracks=20)

# Quit Pygame
pygame.quit()
