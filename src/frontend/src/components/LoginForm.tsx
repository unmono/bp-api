import React, { useState } from 'react';
import { login } from "../api/axiosConfig";

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const token = await login(username, password);
    const cookie_props = {
      path: '/',
      maxAge: 60,
      sameSite: 'strict',
      // httpOnly: true,
      // secure: true,
    }

    document.cookie = `access_token=${token};` +
      Object.entries(cookie_props)
        .map(([key, value]) => `${key}=${value}`)
        .join('; ');
  };

  return (
    <>
      <form onSubmit={handleLogin} className={'loginForm'}>
        <div>
          <label htmlFor="login-input">{'username>'}</label>
          <input
            type="text"
            id="login-input"
            value={ username }
            onChange={(event) => setUsername(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password-input">{'password>'}</label>
          <input
            type="password"
            id="password-input"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
        <button type="submit">#Login</button>
      </form>
    </>
  );
};

export default LoginForm;
