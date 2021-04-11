import {Button, Container, Grid} from "@material-ui/core";
import {Link} from "react-router-dom";
import DescriptionComponent from "../components/DescriptionComponent";


export default function SpotifyLoginScreen() {
    return(
        <div>
            <DescriptionComponent text="In order to create new playlist and add tracks we need you to login into your Spotify account" />
            <Link to="/spotify-redirect">
                <Button variant="contained" color="primary">
                    Login to Spotify
                </Button>
            </Link>
        </div>
    )
}