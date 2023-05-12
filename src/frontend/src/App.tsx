import React, { useState, createContext } from 'react';
import {
  Outlet,
  useNavigate,
} from 'react-router-dom';

import { searchPost, bpGet, login } from './api/axiosConfig';
import './index.css';
import NavBar from "./components/Navbar";
import Modal from "./components/Modal";
import {ProductShortType, SearchQuery} from "./types";
import {
  SubsectionModalContext,
  SearchContext,
  ModalContext,
  LoginContext,
} from './contexts';


function App() {
  const [tkn, setTkn] = useState<string>('');
  const [modalProductsList, setProductsList] = useState<[ProductShortType] | null>(null);
  const navigate = useNavigate();

  const listSubsectionInModal = (subUrl?: string) => () => {
    if(subUrl){
      bpGet(subUrl, tkn).then(response => {
        setProductsList(response);
      });
    } else {
      setProductsList(null);
    }
  }

  const listSearchResultsInModal = (searchQuery: SearchQuery) => {
    searchPost(searchQuery, tkn).then(response => {
      if(response.length === 1) {
        navigate(`/products/${response[0].part_no}`);
        return;
      }
      setProductsList(response);
    })
  }

  const onLogin = async (username: string, password: string) => {
    const token = await login(username, password);
    setTkn(token);
  }

  return (
    <LoginContext.Provider value={ tkn }>
    <SubsectionModalContext.Provider value={ listSubsectionInModal }>
    <SearchContext.Provider value={ listSearchResultsInModal }>
    <ModalContext.Provider value={modalProductsList} >
      <div className={'layout'}>
        <NavBar />
        <Outlet context={{onLogin}}/>
        {modalProductsList && <Modal/>}
      </div>
    </ModalContext.Provider>
    </SearchContext.Provider>
    </SubsectionModalContext.Provider>
    </LoginContext.Provider>
  )
}

export default App;