#!/usr/bin/python

""" jocalado | SPOTIFY API using spotipy: https://spotipy.readthedocs.io/en/2.10.0/"""

import sys
import os
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# access values from ...
try:
    spotify_client_id = os.environ['SPOTIPY_CLIENT_ID']
    spotify_client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
    spotify_username = os.environ['SPOTIPY_USERNAME']
except KeyError as e:
    print(e,"Missing environment variables!")
    exit()

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

print('/n','My Playlists')
user = sp.user(spotify_username)

for k,v in user.items():
    print(k,v)

#top 20 tracks for search q=
print('/n','Daniela Mercury: Top 20 Tracks')
results = sp.search(q='Daniela Mercury', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

#list the names of all the albums released by the artist ‘Oh Wonder’
print('/n','Oh Wonder: All Albums')
artist_uri = 'spotify:artist:5cIc3SBFuBLVxJz58W2tU9'
results = sp.artist_albums(artist_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])

#get 30 second samples and cover art for the top 10 tracks for Led Zeppelin
print('/n','Led Zepplin: 30 sec samples and cover art for TOP 10 Tracks')
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
results = sp.artist_top_tracks(lz_uri)
for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()

#get the URL for an artist image given the artist’s name
print('/n','Daniela Mercury: Cover Art')
artist_name = "Daniela Mercury"
results = sp.search(q='artist:' + artist_name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])

#My Playlist
# print('/n','My Personal Playlist')
# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

results = sp.search(q=artist_name, limit=50)
tids = []
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])
    tids.append(t['uri'])

start = time.time()
features = sp.audio_features(tids)
delta = time.time() - start
for feature in features:
    print(json.dumps(feature, indent=4))
    print()
    analysis = sp._get(feature['analysis_url'])
    print(json.dumps(analysis, indent=4))
    print()
print("features retrieved in %.2f seconds" % (delta,))