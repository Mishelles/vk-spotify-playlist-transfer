import {Grid, Typography} from "@material-ui/core";

export default function DescriptionComponent(props) {
    return (
        <div>
            <Grid container justify="center" alignItems="center" direction="column">
                <Grid item xs={6}>
                    <Typography variant="h3" color="primary" align="center">
                        {props.text}
                    </Typography>
                </Grid>
            </Grid>
        </div>
    )
}