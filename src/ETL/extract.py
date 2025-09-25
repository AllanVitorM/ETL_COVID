import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.utils.constant import IDS
from dotenv import load_dotenv

load_dotenv()

class ExtractSpotify:
    def __init__(self):
        pass

    def extract_data(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=API_SPOTIFY, client_secret=API_SECRET_SPOTIFY)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

        for id in IDS:
            artist = f"https://api.spotify.com/v1/artists/{id}"
            artista_uri = artist.split("/")[-1].split("?")[0]
            data = sp.artists([artista_uri])
            
            for artista in data["artists"]:
                print(artista["name"])
                print(artista["genres"])
                print("Seguidores", artista["followers"]["total"])
                print('  ')
            



