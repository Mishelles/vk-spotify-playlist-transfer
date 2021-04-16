import React from "react";
import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";
import InputComponent from "../components/InputComponent";

export default function VKConfirmationScreen() {
    return (
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent
                text="SMS with confirmation code has been sent. Please, check your phone and enter the code below"/>
            <InputComponent text="Enter code" />
            <ButtonComponent text="CONTINUE" link="/"/>
        </div>
    )
}