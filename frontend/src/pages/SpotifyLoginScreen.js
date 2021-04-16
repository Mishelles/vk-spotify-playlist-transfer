import {Button, Container, Grid} from "@material-ui/core";
import {Link} from "react-router-dom";
import DescriptionComponent from "../components/DescriptionComponent";
import React from "react";


export default function SpotifyLoginScreen() {
    return(
        <div className="main">
            <DescriptionComponent text="In order to create new playlist and add tracks we need you to login into your Spotify account" />
            <Grid container justify="center" alignItems="center" alignContent="center" direction="column">
                <Grid item xs={6} >
                    <Link to="/vk-login">
                        <Button variant="contained" color="primary">
                            LET'S GO
                        </Button>
                    </Link>
                </Grid>
            </Grid>
        </div>
    )
}