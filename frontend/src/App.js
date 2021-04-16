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

function App() {
    return (
      <Router>
          <Route exact path="/" component={WelcomeScreen}/>
          <Route path="/vk-login" component={VKLoginScreen}/>
          <Route path="/spotify-login" component={SpotifyLoginScreen}/>
          <Route path="/vk-confirm" component={VKConfirmationScreen}/>
          <Route path="/spotify-redirect" component={() => { window.location = SPOTIFY_AUTH_URL }}/>
          <Route path="/spotify-callback" component={RedirectPage}/>
      </Router>
    )
}

export default App;
