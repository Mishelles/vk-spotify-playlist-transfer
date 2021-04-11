import {Button, Container, Typography} from "@material-ui/core";
import {Link} from "react-router-dom";


export default function WelcomeScreen() {
    return (
        <div>
            <Typography variant="h1" color="primary">
                kek
            </Typography>
            <Link to="/spotify-login">
                <Button variant="contained" color="primary">
                    Let's go
                </Button>
            </Link>
        </div>
    )
}