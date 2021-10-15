import {
    BrowserRouter as Router,
    Route
} from "react-router-dom"
import WelcomeScreen from "./pages/WelcomeScreen";
import VKLoginScreen from "./pages/VKLoginScreen";
import SpotifyLoginScreen from "./pages/SpotifyLoginScreen";
import RedirectPage from "./pages/RedirectPage";
import VKConfirmationScreen from "./pages/VKConfirmationScreen";
import {SPOTIFY_AUTH_URL} from "./config";
import {useState} from "react";
import {SearchProvider} from './context/SearchContext';
import axios from 'axios';

const axiosInstance = axios.create({
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
    }
});

function App() {
    const [code, setCode] = useState('')
    const setCodeStr = (text) => {
        setCode(text)
    }
    // TODO need final screen or redirection

    const requestTokens = (code) => {
        axios.post(`http://localhost:8000/login/spotify`, {code: code})
            .then(res => {
                console.log(res)
            })
    }

    return (
        <SearchProvider value={{
            setCode: setCodeStr,
            code: code,
            requestTokens: requestTokens
        }}>
            <Router>
                <Route exact path="/" component={WelcomeScreen}/>
                <Route path="/vk-login" component={VKLoginScreen}/>
                <Route path="/spotify-login" component={SpotifyLoginScreen}/>
                <Route path="/vk-confirm" component={VKConfirmationScreen}/>
                <Route path="/spotify-redirect" component={() => {
                    window.location = SPOTIFY_AUTH_URL
                }}/>
                <Route path="/spotify-callback" component={RedirectPage}/>
            </Router>
        </SearchProvider>
    )
}

export default App;
