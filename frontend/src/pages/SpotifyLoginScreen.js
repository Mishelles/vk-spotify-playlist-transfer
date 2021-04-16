import {Button, Container, Grid} from "@material-ui/core";
import {Link} from "react-router-dom";
import DescriptionComponent from "../components/DescriptionComponent";
import React from "react";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";


export default function SpotifyLoginScreen() {
    return(
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent text="In order to create new playlist and add tracks we need you to login into your Spotify account" />
            <ButtonComponent text="LOGIN TO SPOTIFY" link="/spotify-redirect"/>
        </div>
    )
}