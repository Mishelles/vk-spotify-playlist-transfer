import {Button, Container, Typography} from "@material-ui/core";
import {Link} from "react-router-dom";


export default function SpotifyLoginScreen() {
    return(
        <Container maxWidth="sm">
            <Typography variant="h2" color="primary">
                <span>This is Spotify login screen</span>
            </Typography>
            <Link to="/spotify-redirect">
                <Button variant="contained" color="primary">
                    Login to Spotify
                </Button>
            </Link>
        </Container>
    )
}