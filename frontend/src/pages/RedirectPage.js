import React, {useContext, useEffect} from 'react';
import queryString from 'query-string';
import SearchContext from '../context/SearchContext';
import {useHistory} from 'react-router-dom';

export default function RedirectPage(props) {
    let history = useHistory();
    const search = useContext(SearchContext)
    const res = new URLSearchParams(props.location.search).get("code");
    console.log(res)
    useEffect(() => {
        search.setCode(res);
    }, []);
    console.log(search)
    useEffect(() => { // Pass in a callback function!
            search.requestTokens(search.code)
                .then(history.push('/vk-login'));
        },
        []);
    return (
        <div className="redirect">
            {/*<p>{new URLSearchParams(props.location.search).get("code")}</p>*/}
        </div>
    )
}

//TODO after that on the background should be called methods for getting access and refresh tokens
// See 'login_to_spotify' method - tokens should be extracted and saved to creds file

//TODO extract code and save to creds file an authorization code that can be exchanged for an access token.
// (Have your application request authorization; the user logs in and authorizes access)

