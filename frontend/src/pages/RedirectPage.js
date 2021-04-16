import * as queryString from "query-string";
import {useHistory} from "react-router-dom";

export default function RedirectPage(props) {
    let history = useHistory();
    let params = queryString.parse(props.location.search);
    if (params.code !== '') {
        console.log(params.code)
    }
    return (
        <div className="redirect">
            {/*<p>{new URLSearchParams(props.location.search).get("code")}</p>*/}
        </div>
    )
}