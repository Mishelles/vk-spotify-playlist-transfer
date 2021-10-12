import spotify_util as spotify
import vk_util as vk

""" TODO do we need this file? """

vk_util = vk.VkUtil(10)
spotify_util = spotify.SpotifyUtil()

playlist_id = spotify_util.create_playlist_in_spotify()

for batch in vk_util:
    tracks = spotify_util.batch_track_search(batch)
    spotify_util.add_tracks_to_playlist([track['id'] for track in tracks], playlist_id)
