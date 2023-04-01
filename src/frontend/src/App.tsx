import React, { useState, useEffect, createContext } from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';

import { api, searchPost, bpGet } from './api/axiosConfig';
import './index.css';
import NavBar from "./components/Navbar";
import Sections from "./components/Sections";
import Modal from "./components/Modal";
import {ProductShortType, SearchQuery} from "./types";
import ProductInfo from "./components/ProductInfo";

export const SubsectionModalContext = createContext<((subUrl?: string) => () => void) | undefined>(undefined);
export const SearchContext = createContext<((searchQuery: SearchQuery) => void) | null>(null);

function App() {
  const [modalProductsList, setProductsList] = useState<[ProductShortType] | null>(null);

  const listSubsectionInModal = (subUrl?: string) => () => {
    if(subUrl){
      bpGet(subUrl).then(response => {
        setProductsList(response?.data);
      })
    } else {
      setProductsList(null);
    }
  }

  const listSearchResultsInModal = (searchQuery: SearchQuery) => {
    searchPost(searchQuery).then(response => {
      setProductsList(response?.data);
    })
  }

  return (
    <SubsectionModalContext.Provider value={ listSubsectionInModal }>
    <SearchContext.Provider value={ listSearchResultsInModal }>
      <Routes>
        <Route path={'/'} element={<Layout productList={modalProductsList} />}>
          <Route index element={<Sections />} />
          <Route path={'products/:partNum'} element={<ProductInfo />} />
        </Route>
      </Routes>
    </SearchContext.Provider>
    </SubsectionModalContext.Provider>
  )
}

function Layout(props: { productList: [ProductShortType] | null }) {
  return (
    <div className={'layout'}>
      <NavBar />
      <Outlet />
      { props.productList && <Modal productList={ props.productList } /> }
    </div>
  );
}

export default App;

// todo:
//  - error for partnum
//  - api calls error handling
//  - error page
//
