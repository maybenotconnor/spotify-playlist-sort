# -*- coding: utf-8 -*-
"""
Created on Sun June 6 2021

Sort songs in playlists using euclidean distance

@author: Connor C
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import numpy as np
import pp

# Use your own spotify dev data below!
# set open_browser=False to prevent Spotipy from attempting to open the default browser, authenticate with credentials
scope = 'user-library-read user-library-modify playlist-modify-public'

#credentials loaded from .env
load_dotenv('.env')
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
redirect_uri = os.environ.get("redirect_uri")
usernamevar = os.environ.get("usernamevar")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

def getPlaylistID(playlist_name, username=usernamevar):
    #Gets ID of playlist by name
    playlist_id = 'error'
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists user follows
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']
    print("Playlist ID found: ",playlist_id)
    if playlist_id=='error':
        raise
    return playlist_id

def orderTracks(playlist_uri):
    #sort songs based on generated logisitic regression
    error_count = 0
    song_data_input = []

    for song in sp.playlist_tracks(playlist_uri)["items"]:
        try: #get data for song
            song_features = sp.audio_features(song["track"]["id"])
        except: #in case of timeout
            print("Error for track: ", song["track"]["name"])
            error_count += 1 
            continue
        song_data_input.append([song["track"]["name"],song_features[0]["acousticness"],song_features[0]["danceability"],song_features[0]["energy"], song_features[0]["instrumentalness"],song_features[0]["liveness"],song_features[0]["speechiness"],song_features[0]["valence"]])
        print("Added track ",song["track"]["name"]," to list")
    #sort items
    array_full = np.array(song_data_input)
    pp(array_full)
    array_sorted = []
    for x in array_full:
        dist = np.linalg.norm(x[1:])
        x = np.append(x, dist)
        pp(x)
        pp(dist)
        array_sorted.append(x.tolist())

    def distExtract(e):
        return e[-1]

    array_sorted.sort(key=distExtract)
    #array_sorted = array_full[np.argsort(dist)]
    pp(array_sorted)


input = input("Enter playlist name to sort: ")
orderTracks(getPlaylistID(input))