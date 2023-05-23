import React, {useState, useEffect, createContext} from 'react';
import {Outlet} from 'react-router-dom';

import {bpGet} from "./api/axiosConfig";
import './index.css';
import NavBar from "./components/Navbar";

type LoggedContextType = {
  logged: boolean,
  setLogged: any
}

export const LoggedContext =
  createContext<LoggedContextType>({logged: false, setLogged: null});

function App() {
  const [logged, setLogged] = useState<boolean>(false);

  useEffect(() => {
    bpGet('/login/me')
      .then(response => {
        if(response.username) {
          setLogged(true);
        }
      })
      .catch(() => {
        setLogged(false);
      });
  }, []);

  return (
    <LoggedContext.Provider value={{logged: logged, setLogged: setLogged}}>
      <NavBar />
      <div className={'content'}>
        <Outlet />
      </div>
    </LoggedContext.Provider>
  )
}

export default App;