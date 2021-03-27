import requests
import file_important
from pprint import pprint
import json
import sys

class start():


    def __init__(self):
        self.token = file_important.spotfiy_user_token()
        self.api = file_important.spotify_api_key()
        self.id = file_important.spotify_user_id()
        self.headers = {"Content-Type":"application/json","Authorization": f"Bearer {self.token}"}
        self.playlist_id = ''
        self.song_info = {}
        self.uris = []

    def fetch_songs(self):
        params = {'limit':10,'api_key':self.api}
        url = 'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&format=json'

        response = requests.get(url, params=params)
        if response.status_code !=200:
            self.exceptionnal_exception(response.status_code)

        res = response.json()
        song_info = dict()
        for item in res['tracks']['track']:
            song = item['name']
            artist = item['artist']['name']
            song_info[song] = artist
        return song_info

    def get_uri(self, song_info):
        uris = []
        for song_name, artist in song_info.items():
            url = f"https://api.spotify.com/v1/search?query=track%3A{song_name}+{artist}&type=track&offset=0&limit=10"
            response = requests.get(url, headers=self.headers)
            res = response.json()
            output_uri = res['tracks']['items']
            uri = output_uri[0]['uri']
            uris.append(uri)
        return uris
    def create_playlist(self, name, desc):
        data = {
          "name": name,
          "description": desc,
          "public": True
        }
        data = json.dumps(data)
        url = f"https://api.spotify.com/v1/users/{self.id}/playlists"
        response = requests.post(url, data=data , headers= self.headers)

        if response.status_code ==201:
            res = response.json()
            return res['id']
        else:
            self.exceptionnal_exception(response.status_code)

    def add_songs_to_playlist(self, id, uris):
        uri_list = json.dumps(uris)
        url = f"https://api.spotify.com/v1/playlists/{id}/tracks"
        response = requests.post(url , data=uri_list, headers=self.headers)
        if response.status_code == 201:
            return "added successfully"
        else:
            self.exceptionnal_exception(response.status_code)

    def list_songs_in_playlist(self, id):
        url = f"https://api.spotify.com/v1/playlists/{id}/tracks"
        response = requests.get(url , headers = self.headers)
        if response.status_code == 200:
            res = response.json()
            list_song = []
            for item in res['items']:
                list_song.append(item['track']['name'])
            return list_song
        else:
            self.exceptionnal_exception(response.status_code,'error')

    def exceptionnal_exception(self, status_code, err):
        print("Error occured with status code", status_code)
        print("error occured", err)
        sys.exit(0)


