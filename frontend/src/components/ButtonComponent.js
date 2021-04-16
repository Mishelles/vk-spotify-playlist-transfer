import {Button, Grid} from "@material-ui/core";
import {Link} from "react-router-dom";
import React from "react";

export default function ButtonComponent(props) {
    return (
        <Grid container justify="center" alignItems="center" alignContent="center" direction="column">
            <Grid item xs={6} >
                <Link to={props.link}>
                    <Button variant="contained" color="primary">
                        {props.text}
                    </Button>
                </Link>
            </Grid>
        </Grid>
    )
}