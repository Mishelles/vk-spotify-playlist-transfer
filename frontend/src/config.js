export const SPOTIFY_REDIRECT_URI = "http://localhost:3000/spotify-callback"
export const SPOTIFY_CLIENT_ID = "e05199b79be74402bb779d6d9dd9fbdf"
export const SPOTIFY_AUTH_URL = `https://accounts.spotify.com/authorize?client_id=${SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri=${SPOTIFY_REDIRECT_URI}&scope=playlist-modify-private`
