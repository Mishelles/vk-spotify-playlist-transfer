import React from 'react'

const SearchContext = React.createContext({
    code: '',
    vkLogin: '',
    vkPass: '',
    setCodeStr: (text) => {},
    setLoginStr: (text) => {},
    setPassStr: (text) => {},
    requestTokens: (code) => {},
    loginToVk: (vkLogin, vkPass) => {},
})

export const SearchProvider = SearchContext.Provider

export default SearchContext