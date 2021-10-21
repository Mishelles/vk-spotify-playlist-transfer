import {Button, Grid, makeStyles} from "@material-ui/core";
import {Link} from "react-router-dom";
import React from "react";

const useStyles = makeStyles({
    root: {
        background: '#1DB954',
        boxShadow: '0 0 35px 3px rgba(0, 0, 0, 0.29)',
        borderRadius: '35px',
        color: '#FFF',
        marginTop: '50px',
        "&:hover, &:focus": {
            background: '#22e06b'
        },
        width: '250px',
        fontSize: 18,
        fontWeight: 600,
        backdropFilter: 'blur(2.84419px)',
    },
});

export default function ButtonComponent(props) {
    const classes = useStyles();

    return (
        <Grid container onClick={(event) => props.onClick(event)} justify="center" alignItems="center" alignContent="center" direction="column" >
            <Grid item xs={12}>
                <Link to={props.link}>
                    <Button variant="contained" color="inherit"  classes={{
                        root: classes.root,
                    }}>
                        {props.text}
                    </Button>
                </Link>
            </Grid>
        </Grid>
    )
}