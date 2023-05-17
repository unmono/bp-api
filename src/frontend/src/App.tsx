import React from 'react';
import {
  Outlet,
} from 'react-router-dom';

import './index.css';
import NavBar from "./components/Navbar";


function App() {

  return (
    <>
      <NavBar />
      <div className={'content'}>
        <Outlet />
      </div>
    </>
  )
}

export default App;