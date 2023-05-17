import { NavLink } from 'react-router-dom';

type NavLinkProps = {
  to: string,
  regularClass: string,
  activeClass: string,
  text: string
}

export default function (props: NavLinkProps) {
  return (
    <NavLink
      to={props.to} end
      className={ ({isActive}) =>
        isActive ? props.activeClass : props.regularClass
      }
    >{props.text}</NavLink>
  );
}