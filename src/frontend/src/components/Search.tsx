import React, { useContext, useState } from 'react';
import {SearchContext} from "../contexts";

export default function () {
  const [searchInput, setSearchInput] = useState('');
  const listSearchResultsInModal = useContext(SearchContext);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const r = new RegExp(/^([A-Z0-9]*[?]?[A-Z0-9]*){0,4}$/i);
    if(r.test(e.target.value)) {
      setSearchInput(e.target.value);
    }
  }

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if(searchInput.length === 10 && listSearchResultsInModal) {
      const searchQuery = { search_query: searchInput }
      listSearchResultsInModal(searchQuery);
    }
  }

  // Enter click
  return(
    <div className={'search'}>
      <form onSubmit={ handleSearchSubmit }>
        <input
          type={'text'}
          placeholder={'Search'}
          maxLength={10}
          size={10}
          value={searchInput}
          onChange={ handleSearchChange }
        />
        <button type={'submit'}>do</button>
      </form>
    </div>
  );
}
