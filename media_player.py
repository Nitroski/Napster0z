import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
import time

def on_player_state_changed(state):
    current_track = state['track_window']['current_track']
    track_name = current_track['name']
    artist_names = ', '.join([artist['name'] for artist in current_track['artists']])
    print('Current track:', track_name)
    print('Artist(s):', artist_names)
    # Update UI with current track info
    update_ui(track_name, artist_names)

def update_ui(track_name, artist_names):
    pygame.display.set_caption("Current Track: {} - Artist(s): {}".format(track_name, artist_names))
    # You can further customize the UI update based on your preferences

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Spotify authentication
scope = "user-read-playback-state,user-modify-playback-state"
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Connect to the player
if sp.current_user():
    print('Successfully connected to Spotify!')
else:
    print('Failed to connect to Spotify. Please check your authentication.')

# Add event listeners for playback controls
sp.current_playback(market=None)  # This triggers the event listener for playback state change

# Start event loop to periodically check for playback state
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    state = sp.current_playback(market=None)
    if state:
        on_player_state_changed(state)

    time.sleep(1)  # Adjust the sleep time as needed

pygame.quit()
