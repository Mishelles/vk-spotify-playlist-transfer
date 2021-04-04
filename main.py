import spotify_util as spotify
import vk_util as vk

'''
    Execute steps:
        1. Get VK token
        2. Get Spotify root token
        3. Create playlist at Spotify
        4. Get first 200 tracks from VK
        5. Find 200 tracks at Spotify
        6. Add 200 tracks to playlist
        7. Repeat steps 4-6 till we get all tracks.
'''

vk_util = vk.VkUtil(10)
spotify_util = spotify.SpotifyUtil()

playlist_id = spotify_util.create_playlist_in_spotify()

for batch in vk_util:
    tracks = spotify_util.batch_track_search(batch)
    spotify_util.add_tracks_to_playlist([track['id'] for track in tracks], playlist_id)
