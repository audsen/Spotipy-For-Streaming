import polling
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def update_content(current_song):
    with open("scrolling_text.txt", 'w', encoding="utf-8") as content:
        content.write("streams are Tuesday, Sunday @ 6pm MST \t ★ \t" +
                      " now playing: " + current_song["item"]["name"] + "— " +
                      current_song["item"]["album"]["name"] + " \t ★ \t")
        
    # alternative content fill w/ artist name instead of album name
    # for situations where that matters
    
#    with open("scrolling_text.txt", 'w', encoding="utf-8") as content:
#        content.write("streams are Tuesday, Sunday @ 6pm MST \t ★ \t" +
#                      " now playing: " + current_song["item"]["name"] + "— " +
#                      current_song["item"]["artists"][0]["name"] + " \t ★ \t")

def initialize_data():
    with open("spotipy_auth.json", 'r') as f:
        data = json.load(f)
    return([data["cid"],data["secret"]])

def api_listener(spotify_obj, current_song):
    try:
        polling.poll(
            lambda: (spotify_obj.currently_playing())["item"]["id"] != current_song["item"]["id"],
            step=1,
            poll_forever=True
        )
        return spotify_obj.currently_playing()
    except Exception as e:
        print(f"Error during polling: {e}")

    return None

def main():
    data = initialize_data()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=data[0],client_secret=data[1],
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read user-read-currently-playing user-read-playback-state"))

    current_song = sp.currently_playing()
    update_content(current_song)

    # NOTE: No error handling if nothing is playing
    # just make sure you have Spotify running before
    # starting the script mkay :)

    print("Initialization complete\nPolling Spotify API")
    
    while True:
        current_song = api_listener(sp, current_song)
        if current_song is not None:
            update_content(current_song)
        time.sleep(5)

if __name__ == "__main__":
    main()
