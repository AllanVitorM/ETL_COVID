import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .constant import IDS
from dotenv import load_dotenv

load_dotenv()

class Search:
    def __init__(self):
        pass
    
    def SearchArtist(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=API_SPOTIFY, client_secret=API_SECRET_SPOTIFY)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        result = sp.search(q="Temple Of The Dog", type="artist", limit=1)
        artist = result["artists"]["items"][0]
        print(artist["id"], artist["name"])
        
        
    def SearchAlbuns(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=API_SPOTIFY, client_secret=API_SECRET_SPOTIFY)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        for i, id in enumerate(IDS):
            result = sp.artist_albums(id, album_type="album", limit=20)
            artists = [items['artists'] for items in result['items']]
            print(artists[0][0]['name'])
            print([item['name'] for item in result["items"]])
            print('    ')
               
    def SearchTracksPop(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=API_SPOTIFY, client_secret=API_SECRET_SPOTIFY)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        for id in IDS:
            result = sp.artist_top_tracks(id, country="US")
            artista_nome = sp.artist(id)["name"]
            for track in result['tracks']:
                print(f"Nome da banda {artista_nome}: {track['name']} ({track['popularity']} de popularidade)")

            
