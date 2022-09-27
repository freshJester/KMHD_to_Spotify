import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from urllib.request import urlopen
import time

# Run these before running the script
# source ./spotipy/Scripts/activate
# export SPOTIPY_CLIENT_ID=8e3bd334faab4a5e85eb5c866180ec52 && export SPOTIPY_CLIENT_SECRET=1c30efaa5eb04519b932c867e27ac086 && export SPOTIPY_REDIRECT_URI=https://localhost:8888/callback

prev_song_ids = []

def spotify_run_query_and_add_to_playlist(song, artist):
    global prev_song_id
    if song != "" and artist != "":
        try:
            results = sp.search(q='track:' + song + ', artist:' + artist, type='track,artist', limit=1)  # Query for song

            # Error handling attempts
            # print(results)
            # for thing in results:
            #     print(thing)
            # print(results['tracks'])

            song_id = results['tracks']['items'][0]['id']  # Get song ID from query

            if song_id not in prev_song_ids:
                print(artist, "-", song, "has been added!")
                sp.playlist_add_items('6DiobUvq9mwFpHHb17sV8B', [song_id])  # Add song to the 'KMHD Scraper' playlist
                prev_song_ids.append(song_id)
        except Exception as e:
            print("Error encountered: ", e)
            # Further attempts at adding the track eventually?
            # try:
            #     results = sp.search(q='artist:' + artist, type='artist')
            #     print(results)
            # except Exception as e1:
            #     print("Error encountered: ", e2)


# playlists = sp.user_playlists('freshjay2000')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['id'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None


if __name__ == "__main__":

    while True:
        #  Pull song from KMHD query, split up the query and get the artist and song name
        url = "https://yp.cdnstream1.com/metadata/2442_64/current.json?cb=708090"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        try:
            html = html.strip("\"").split(":")
            song = html[2].split("\"")[1].rstrip(" ").lstrip(" ")
            artist = html[3].split("\"")[1].rstrip(" ").lstrip(" ")
            print(artist, "-", song, "heard, attempting to add...")

            #  Authorize use of this spotify user's playlist
            #auth_manager = SpotifyClientCredentials()
            auth_manager = SpotifyOAuth(scope='playlist-modify-public')
            sp = spotipy.Spotify(auth_manager=auth_manager)

            spotify_run_query_and_add_to_playlist(song, artist)

            #  More string parsing
            if 'and' in artist:
                try:
                    artist = artist.split(' and ')
                    artist = artist[0] + ', ' + artist[1] 
                    spotify_run_query_and_add_to_playlist(song, artist)
                except Exception as e:
                    print("Error encountered: ", e)
            elif '&' in artist:
                try:
                    artist = artist.split(' & ')
                    artist = artist[0] + ', ' + artist[1] 
                    spotify_run_query_and_add_to_playlist(song, artist)
                except Exception as e:
                    print("Error encountered: ", e)
        except Exception as e:
            print("Error encountered: ", e)

        time.sleep(30)  # Rest for a bit, few songs are less than 30 seconds