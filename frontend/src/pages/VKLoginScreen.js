import {
    Button,
    FormControl, Grid,
    IconButton,
    Input,
    InputAdornment,
    InputLabel,
    makeStyles,
    Typography
} from "@material-ui/core";
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';
import clsx from 'clsx';
import React from "react";
import {Link, useHistory} from 'react-router-dom'
import DescriptionComponent from "../components/DescriptionComponent";
import ButtonComponent from "../components/ButtonComponent";
import LogosComponent from "../components/LogosComponent";
import InputComponent from "../components/InputComponent";

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
        setValues({ ...values, showPassword: !values.showPassword });
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
            <DescriptionComponent text="Now you need to login into your VK account" />
            <InputComponent text="Email or phone number" />
            <InputComponent text="Password" />
            <ButtonComponent text="LOGIN TO VK" link="/vk-confirm"/>
        </div>
    )
}