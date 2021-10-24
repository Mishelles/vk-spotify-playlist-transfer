import {
    Grid,
    makeStyles,
    Typography
} from "@material-ui/core";
import React, {useContext} from "react";
import {useHistory} from 'react-router-dom'
import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";
import {withStyles} from "@material-ui/core/styles";
import CustomInput from "../components/CustomInput";
import SearchContext from "../context/SearchContext";

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    margin: {
        margin: theme.spacing(1),
    },
    withoutLabel: {
        marginTop: theme.spacing(3),
    },
    textField: {
        width: '25ch',
    },
}));

const WhiteTextTypography = withStyles({
    root: {
        color: "#f2f2f2",
        lineHeight: '20px',
        maxWidth: '70%'
    }
})(Typography);

export default function VKLoginScreen() {
    const search = useContext(SearchContext);
    let history = useHistory();

    const handleLoginButtonClick = async () => {
        console.log('kek')
        await search.loginToVk(search.vkLogin, search.vkPass);
        history.push('/progress');
    }

    return (
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent text="Now you need to login into your VK account"/>
            <CustomInput onChange={e => search.setLoginStr(e.target.value)} text="Email or phone number" type="text"/>
            <CustomInput onChange={e => search.setPassStr(e.target.value)} text="Password" type="password"/>
            <ButtonComponent onClick={async () => await handleLoginButtonClick()} text="LOGIN TO VK"/>
            <div className="disclaimer">
                <Grid container justify="center" alignItems="center" direction="row">
                    <WhiteTextTypography variant="p" align="center">
                        *Do not worry about your login credentials safety. We need them only to access limiteed VK
                        music API. After login you’ll receive a security alert from VK about login attempt from
                        Android device. This is a normal behaviour. If you don’t trust, you can change your password
                        at any time.
                    </WhiteTextTypography>

                </Grid>
            </div>
        </div>
    )
}