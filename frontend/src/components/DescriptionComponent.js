import {Grid, Typography} from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";

const WhiteTextTypography = withStyles({
    root: {
        color: "#f2f2f2"
    }
})(Typography);

export default function DescriptionComponent(props) {
    return (
        <div className="DescriptionComponent">
            <Grid container justify="center" alignItems="center" direction="column">
                <Grid item xs={10} sm={6}>
                    <WhiteTextTypography variant="h3" align="center">
                        {props.text}
                    </WhiteTextTypography>
                </Grid>
            </Grid>
        </div>
    )
}