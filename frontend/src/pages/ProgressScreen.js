import React, {useContext} from "react";
import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";
import InputComponent from "../components/InputComponent";
import SearchContext from "../context/SearchContext";
import {useHistory} from "react-router-dom";

export default function ProgressScreen() {
    const search = useContext(SearchContext);
    let history = useHistory();

    const handleLoginButtonClick = async () => {
        await search.initProcess();
        history.push('/progress');
    }

    return (
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent
                text="This a page showing application progress"/>
            <ButtonComponent onClick={async () => await handleLoginButtonClick()} text="CONTINUE" />
        </div>
    )
}