import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import React from "react";
import LogosComponent from "../components/LogosComponent";


export default function WelcomeScreen() {
    return (
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent text="Hello! This app will help you to transfer your VK music into Spotify playlist in 3 easy steps" />
            <ButtonComponent text="LET'S GO" link="/spotify-login"/>
        </div>
    )
}