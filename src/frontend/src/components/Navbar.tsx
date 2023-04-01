import Search from "./Search";
import SectionsButton from "./SectionsButton";

export default function NavBar () {
  return (
    <nav>
      <SectionsButton />
      <Search />
    </nav>
  );
}