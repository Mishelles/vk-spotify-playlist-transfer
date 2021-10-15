import React from 'react'

const SearchContext = React.createContext({
    code: ''

})

export const SearchProvider = SearchContext.Provider

export default SearchContext