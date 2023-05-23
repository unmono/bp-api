import { useState, useEffect, useContext } from 'react';

import {bpGet} from "../api/axiosConfig";
import { LoggedContext } from "../App";

export default function LoginGreetings () {
  const { logged } = useContext(LoggedContext);
  const [username, setUsername] = useState<string>('');

  useEffect(() => {
    if(logged) {
      bpGet('/login/me')
        .then(response => {
          if(response.username) {
            setUsername(response.username);
          }
        })
    }
  }, [])

  return (
    <p className={'greetings'}>
      Hi, {username}
    </p>
  )
}