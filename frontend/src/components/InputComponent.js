import {FormControl, Grid, makeStyles, TextField} from "@material-ui/core";
import clsx from "clsx";
import React from "react";
import {useHistory} from "react-router-dom";

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
        width: '355px',
        height: '50px'
    },
    margin: {
        margin: theme.spacing(1),
    },
    withoutLabel: {
        marginTop: theme.spacing(3),
    },
    textField: {
        width: '355px',
        height: '50px'
    },
}));

export default function InputComponent(props) {

    const classes = useStyles();
    let history = useHistory();

    const [values, setValues] = React.useState({
        code: ''
    });

    const handleChange = (prop) => (event) => {
        setValues({...values, [prop]: event.target.value});
    };

    return (
        <Grid container justify="center" alignItems="center" alignContent="center" direction="column">
            <Grid item xs={6}>
                <FormControl className={clsx(classes.margin, classes.withoutLabel, classes.textField)}>
                    <TextField
                        className="inputField"
                        id="standard-adornment-weight"
                        label={props.text}
                        variant="outlined"
                        value={values.code}
                        onChange={handleChange('code')}
                        aria-describedby="standard-weight-helper-text"
                        inputProps={{
                            'aria-label': 'code',
                        }}
                    />
                </FormControl>
            </Grid>
        </Grid>
    )
}