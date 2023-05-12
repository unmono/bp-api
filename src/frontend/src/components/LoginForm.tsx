import React, { useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import PartnumPlaceholder from "./PartnumPlaceholder";

type LoginFormProps = {
  onLogin: (login: string, password: string) => void;
};

const LoginForm: React.FC = () => {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const { onLogin } = useOutletContext<LoginFormProps>();

  const handleLogin = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onLogin(login, password);
  };

  return (
    <>
      <PartnumPlaceholder />
      <form onSubmit={handleLogin}>
        <div>
          <label htmlFor="login-input">Login:</label>
          <input
            type="text"
            id="login-input"
            value={login}
            onChange={(event) => setLogin(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password-input">Password:</label>
          <input
            type="password"
            id="password-input"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </>
  );
};

export default LoginForm;
