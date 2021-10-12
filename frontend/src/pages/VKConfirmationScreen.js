import React from "react";
import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";
import InputComponent from "../components/InputComponent";

export default function VKConfirmationScreen() {
    //TODO here on the background should be launched methods '_prepare_vk_session' (auth code should be passed) and 'get_total_tracks' from vk_util.py
    return (
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent
                text="SMS with confirmation code has been sent. Please, check your phone and enter the code below"/>
            <InputComponent text="Enter code" />
            <ButtonComponent text="CONTINUE" link="/"/>
        </div>
    )
    // TODO it seems to be the latest screen, so here should be also placed a progress bar (?) or at
    //  least redirection to the spotify playlist should be implemented (ex. https://open.spotify.com/{playlistID_from__create_playlist_in_spotify__method})
}