import {
  BrowserRouter as Router,
  Route
} from "react-router-dom"
import './App.css';
import WelcomeScreen from "./pages/WelcomeScreen";
import VKLoginScreen from "./pages/VKLoginScreen";
import SpotifyLoginScreen from "./pages/SpotifyLoginScreen";
import VKConfirmationScreen from "./pages/VKConfirmationScreen";

function App() {
    return (
      <Router>
          <Route exact path="/" component={WelcomeScreen}/>
          <Route path="/vk-login" component={VKLoginScreen}/>
          <Route path="/spotify-login" component={SpotifyLoginScreen}/>
          <Route path="/vk-confirm" component={VKConfirmationScreen}/>
          <Route path="/spotify-redirect" component={() => { window.location = 'https://google.com' }}/>
          <Route path="/spotify-callback" component={() => { console.log("kek") }}/>
      </Router>
    )
}

export default App;
