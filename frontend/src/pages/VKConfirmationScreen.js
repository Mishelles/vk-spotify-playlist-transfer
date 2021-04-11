import clsx from "clsx";
import {Button, FormControl, Input, InputAdornment, makeStyles, Typography} from "@material-ui/core";
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

export default function VKConfirmationScreen() {
    const classes = useStyles();
    let history = useHistory();

    const [values, setValues] = React.useState({
        code: ''
    });

    const handleChange = (prop) => (event) => {
        setValues({...values, [prop]: event.target.value});
    };

    const handleButtonOnClick = (event) => {
        history.push('/');
    };

    return (
        <div>
            <DescriptionComponent text="SMS with confirmation code has been sent. Please, check your phone and enter the code below" />
            <FormControl className={clsx(classes.margin, classes.withoutLabel, classes.textField)}>
                <Input
                    id="standard-adornment-weight"
                    value={values.code}
                    onChange={handleChange('code')}
                    endAdornment={<InputAdornment position="end">Code</InputAdornment>}
                    aria-describedby="standard-weight-helper-text"
                    inputProps={{
                        'aria-label': 'code',
                    }}
                />
            </FormControl>
            <Button variant="contained" color="primary" onClick={handleButtonOnClick}>
                Login
            </Button>
        </div>
    )
}