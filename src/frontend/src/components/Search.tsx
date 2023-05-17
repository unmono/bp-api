import React, { useContext, useState } from 'react';
import {useNavigate} from 'react-router-dom';
// import {SearchContext} from "../contexts";

export default function () {
  const [searchInput, setSearchInput] = useState('');
  const navigate = useNavigate();
  const r = new RegExp(/^([A-Z0-9]*[?]?[A-Z0-9]*){0,4}$/i);
  // const listSearchResultsInModal = useContext(SearchContext);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if(r.test(e.target.value)) {
      setSearchInput(e.target.value);
    }
  }

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if(searchInput.length === 10 && r.test(searchInput)) {
      navigate('/products/search', {
        state: {
          searchQuery: searchInput
        }
      })
    //   const searchQuery = { search_query: searchInput }
    //   listSearchResultsInModal(searchQuery);
    }
  }

  // Enter click
  return(
    <form onSubmit={ handleSearchSubmit }>
      <input
        type={'text'}
        maxLength={10}
        size={10}
        value={searchInput}
        onChange={ handleSearchChange }
        className={'search-input'}
      />
      <button type={'submit'} className={'search-submit'}>#Search</button>
    </form>
  );
}
