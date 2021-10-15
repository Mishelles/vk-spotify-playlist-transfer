import React, {useContext, useEffect} from 'react';
import queryString from 'query-string';
import SearchContext from '../context/SearchContext';
import {useHistory} from 'react-router-dom';

export default function RedirectPage(props) {
    let history = useHistory();
    let params = queryString.parse(props.location.search);
    const search = useContext(SearchContext)
    if (params.code !== '') {
        search.setCode(new URLSearchParams(props.location.search).get("code"))
        search.requestTokens(search.code)
        setTimeout(() => {
            history.push('/vk-login')
        }, 2000)
    }
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

