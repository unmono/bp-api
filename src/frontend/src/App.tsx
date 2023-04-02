import React, { useState, createContext } from 'react';
import {
  Outlet,
  useNavigate,
} from 'react-router-dom';

import { searchPost, bpGet } from './api/axiosConfig';
import './index.css';
import NavBar from "./components/Navbar";
import Modal from "./components/Modal";
import {ProductShortType, SearchQuery} from "./types";

export const SubsectionModalContext =
  createContext<((subUrl?: string) => () => void) | undefined>(undefined);

export const SearchContext =
  createContext<((searchQuery: SearchQuery) => void) | null>(null);

export const ModalContext =
  createContext<[ProductShortType] | null>(null);

function App() {
  const [modalProductsList, setProductsList] = useState<[ProductShortType] | null>(null);
  const navigate = useNavigate();

  const listSubsectionInModal = (subUrl?: string) => () => {
    if(subUrl){
      bpGet(subUrl).then(response => {
        setProductsList(response);
      });
    } else {
      setProductsList(null);
    }
  }

  const listSearchResultsInModal = (searchQuery: SearchQuery) => {
    searchPost(searchQuery).then(response => {
      if(response.length === 1) {
        navigate(`/products/${response[0].part_no}`);
        return;
      }
      setProductsList(response);
    })
  }

  return (
    <SubsectionModalContext.Provider value={ listSubsectionInModal }>
    <SearchContext.Provider value={ listSearchResultsInModal }>
    <ModalContext.Provider value={modalProductsList} >
      <div className={'layout'}>
        <NavBar />
        <Outlet />
        {modalProductsList && <Modal/>}
      </div>
    </ModalContext.Provider>
    </SearchContext.Provider>
    </SubsectionModalContext.Provider>
  )
}

export default App;