import React from 'react'

const SearchContext = React.createContext({
    code: '',
    setCode: (text) => {},
    requestTokens: (code) => {},

})

export const SearchProvider = SearchContext.Provider

export default SearchContext