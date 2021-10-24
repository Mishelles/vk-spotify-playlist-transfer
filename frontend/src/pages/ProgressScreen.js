import React from "react";
import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";
import InputComponent from "../components/InputComponent";

export default function ProgressScreen() {
    return (
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent
                text="This a page showing application progress"/>
            <ButtonComponent text="CONTINUE" link="/"/>
        </div>
    )
}