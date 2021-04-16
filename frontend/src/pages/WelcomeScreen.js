import {Button, Grid} from "@material-ui/core";
import {Link} from "react-router-dom";
import DescriptionComponent from "../components/DescriptionComponent";


export default function WelcomeScreen() {
    return (
        <div className="main">
            <DescriptionComponent text="Hello! This app will help you to transfer your VK music into Spotify playlist in 3 easy steps" />
            <Grid container justify="center" alignItems="center" alignContent="center" direction="column">
                <Grid item xs={6} >
                    <Link to="/spotify-login">
                        <Button variant="contained" color="primary">
                            LET'S GO
                        </Button>
                    </Link>
                </Grid>
            </Grid>
        </div>
    )
}