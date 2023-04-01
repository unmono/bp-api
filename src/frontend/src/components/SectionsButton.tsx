import { NavLink } from 'react-router-dom';

export default function () {
  return (
    <NavLink
      to={'/'} end
      className={ ({isActive}) =>
        isActive ? 'section-button section-button-active' : 'section-button'
      }
    >
      <span></span>
      <span></span>
      <span></span>
    </NavLink>
  );
}