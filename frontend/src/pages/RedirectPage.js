import React, {useContext, useEffect} from 'react';
import SearchContext from '../context/SearchContext';
import {useHistory} from 'react-router-dom';

export default function RedirectPage(props) {
    let history = useHistory();
    const search = useContext(SearchContext)

    useEffect(() => { // Pass in a callback function
            const res = new URLSearchParams(props.location.search).get("code");
            search.setCodeStr(res);
            search.requestTokens(res)
                .then(history.push('/vk-login'));
        },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        []);
    return (
        <div className="redirect">
            {/*<p>{new URLSearchParams(props.location.search).get("code")}</p>*/}
        </div>
    )
}

