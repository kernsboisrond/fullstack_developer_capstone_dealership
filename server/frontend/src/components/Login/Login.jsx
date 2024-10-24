import React, { useState } from 'react';
import "./Login.css";
import Header from '../Header/Header';

const Login = ({ onClose }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [open, setOpen] = useState(true);

  let login_url = window.location.origin + "/djangoapp/login/";  // Add trailing slash

  const login = async (e) => {
    e.preventDefault();

    const res = await fetch(login_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,  // Correct field name
        password: password   // Correct field name
      }),
    });

    const json = await res.json();
    if (json.status === "success") {  // Check for correct status
      sessionStorage.setItem('username', json.username);  // Store username
      setOpen(false);        
    } else {
      alert("The user could not be authenticated. " + json.message);
    }
  };

  if (!open) {
    window.location.href = "/";
  }

  return (
    <div>
      <Header />
      <div onClick={onClose}>
        <div
          onClick={(e) => {
            e.stopPropagation();
          }}
          className='modalContainer'
        >
          <form className="login_panel" onSubmit={login}>
            <div>
              <span className="input_field">Username </span>
              <input
                type="text"
                name="username"
                placeholder="Username"
                className="input_field"
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div>
              <span className="input_field">Password </span>
              <input
                name="password"
                type="password"
                placeholder="Password"
                className="input_field"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div>
              <input className="action_button" type="submit" value="Login" />
              <input
                className="action_button"
                type="button"
                value="Cancel"
                onClick={() => setOpen(false)}
              />
            </div>
            <a className="loginlink" href="/register">Register Now</a>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
