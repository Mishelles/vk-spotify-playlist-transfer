import {Button, Grid} from "@material-ui/core";
import React from "react";

export default function LogosComponent(props) {
    return (
        <Grid container justify="center" alignItems="center" alignContent="center" direction="column" >
            <Grid container alignItems="center" alignContent="center" xs={4} direction="row" wrap="nowrap">
                <Grid item container justify="center">
                    <img src="vk-logo.png" alt="Vk logo" width="100px" className="logo"/>
                </Grid>
                <Grid item container justify="center">
                    <svg width="130" height="75" viewBox="0 0 130 75" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M127.787 41.283C129.738 39.329 129.736 36.1632 127.782 34.212L95.9396 2.41439C93.9857 0.463128 90.8198 0.465339 88.8686 2.41932C86.9173 4.37331 86.9195 7.53913 88.8735 9.49039L117.178 37.7549L88.913 66.0589C86.9618 68.0129 86.964 71.1787 88.9179 73.13C90.8719 75.0812 94.0378 75.079 95.989 73.125L127.787 41.283ZM0.503491 42.8364L124.252 42.75L124.245 32.75L0.496509 32.8364L0.503491 42.8364Z"
                            fill="#FFF9F9" fill-opacity="0.8"/>
                    </svg>
                </Grid>
                <Grid item container justify="center">
                    <img src="sp-logo.png" alt="SP logo" width="100px" className="logo"/>
                </Grid>
            </Grid>
        </Grid>
    )
}