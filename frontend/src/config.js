export const SPOTIFY_REDIRECT_URI = "http://localhost:3000/spotify-callback"
//TODO It's yours, by mine is not working, wtf (e05199b79be74402bb779d6d9dd9fbdf)
export const SPOTIFY_CLIENT_ID = "4c32a64257404c37958b207fede9e902"
export const SPOTIFY_AUTH_URL = `https://accounts.spotify.com/authorize?client_id=${SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri=${SPOTIFY_REDIRECT_URI}&scope=playlist-modify-private`
