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
          <Route exact path="/vk-login" component={VKLoginScreen}/>
          <Route exact path="/spotify-login" component={SpotifyLoginScreen}/>
          <Route exact path="/vk-confirm" component={VKConfirmationScreen}/>
      </Router>
    )
}

export default App;
