import { useContext } from 'react';
import Cookies from 'js-cookie';

import { LoggedContext } from "../App";
import Search from "./Search";
import NavButton from "./NavButton";

export default function NavBar () {
  const { logged, setLogged } = useContext(LoggedContext);

  const logout = () => {
    Cookies.remove('access_token');
    setLogged(false);
  }

  const logoutButton = (
    <button
      className={'logout-link'}
      onClick={logout}
    >
      #Logout
    </button>
  );
  const loginButton = (
    <NavButton
      to={'/login'}
      regularClass={'nav-links'}
      activeClass={'nav-links nav-links-active'}
      text={'#Login'}
    />
  )

  return (
    <nav>
      <div>
        <NavButton
          to={'/'}
          regularClass={'nav-links'}
          activeClass={'nav-links nav-links-active'}
          text={'#Sections'}
        />
        { logged ? logoutButton : loginButton }
      </div>
      <Search />
    </nav>
  );
}