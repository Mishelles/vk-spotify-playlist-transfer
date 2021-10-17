import React from 'react'

const SearchContext = React.createContext({
    code: '',
    setCodeStr: (text) => {},
    requestTokens: (code) => {},

})

export const SearchProvider = SearchContext.Provider

export default SearchContext