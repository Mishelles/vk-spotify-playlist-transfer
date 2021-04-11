import {
    Button,
    FormControl,
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
import { useHistory } from 'react-router-dom'
import DescriptionComponent from "../components/DescriptionComponent";

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
        <div>
            <DescriptionComponent text="Now you need to login into your VK account" />
            <FormControl className={clsx(classes.margin, classes.withoutLabel, classes.textField)}>
                <Input
                    id="standard-adornment-weight"
                    value={values.login}
                    onChange={handleChange('login')}
                    endAdornment={<InputAdornment position="end">Login</InputAdornment>}
                    aria-describedby="standard-weight-helper-text"
                    inputProps={{
                        'aria-label': 'login',
                    }}
                />
            </FormControl>
            <FormControl className={clsx(classes.margin, classes.textField)}>
                <InputLabel htmlFor="standard-adornment-password">Password</InputLabel>
                <Input
                    id="standard-adornment-password"
                    type={values.showPassword ? 'text' : 'password'}
                    value={values.password}
                    onChange={handleChange('password')}
                    endAdornment={
                        <InputAdornment position="end">
                            <IconButton
                                aria-label="toggle password visibility"
                                onClick={handleClickShowPassword}
                                onMouseDown={handleMouseDownPassword}
                            >
                                {values.showPassword ? <Visibility /> : <VisibilityOff />}
                            </IconButton>
                        </InputAdornment>
                    }
                />
            </FormControl>
            <Button variant="contained" color="primary" onClick={handleButtonOnClick}>
                Login
            </Button>
        </div>
    )
}