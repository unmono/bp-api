import Search from "./Search";
import NavButton from "./NavButton";

export default function NavBar () {
  return (
    <nav>
      <div>
        <NavButton
          to={'/'}
          regularClass={'nav-links'}
          activeClass={'nav-links nav-links-active'}
          text={'#Sections'}
        />
        <NavButton
          to={'/login'}
          regularClass={'nav-links'}
          activeClass={'nav-links nav-links-active'}
          text={'#Login'}
        />
      </div>
      <Search />
    </nav>
  );
}