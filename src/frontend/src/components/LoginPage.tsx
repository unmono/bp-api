import { useContext } from 'react';

import { LoggedContext } from "../App";
import LoginForm from './LoginForm';
import LoginGreetings from "./LoginGreetings";

export default function LoginPage() {
  const {logged} = useContext(LoggedContext);

  const toRender = logged ? <LoginGreetings/> : <LoginForm/>;

  return (
    <>{ toRender }</>
  )
}