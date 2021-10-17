import {
    Grid,
    makeStyles,
    Typography
} from "@material-ui/core";
import React from "react";
import {useHistory} from 'react-router-dom'
import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";
import {withStyles} from "@material-ui/core/styles";
import CustomInput from "../components/CustomInput";

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
    let history = useHistory();

    const [values, setValues] = React.useState({
        login: '',
        password: '',
        showPassword: false,
    });

    const handleChange = (prop) => (event) => {
        setValues({...values, [prop]: event.target.value});
    };
    const classes = useStyles();

    const handleClickShowPassword = () => {
        setValues({...values, showPassword: !values.showPassword});
    };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

    const handleButtonOnClick = (event) => {
        history.push('/vk-confirm');
    };

    return (
        <div className="main">
            <LogosComponent/>
            <DescriptionComponent text="Now you need to login into your VK account"/>
            <CustomInput text="Email or phone number"/>
            <CustomInput text="Password" type="password"/>
            <ButtonComponent text="LOGIN TO VK" link="/vk-confirm"/>
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