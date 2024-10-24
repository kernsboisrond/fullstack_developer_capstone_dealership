import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [open, setOpen] = useState(true); // To handle modal close

  let register_url = window.location.origin + "/djangoapp/register/";  // Ensure the URL matches backend

  const register = async (e) => {
    e.preventDefault();

    const res = await fetch(register_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userName: userName,  // Ensure the backend is expecting 'userName'
        password: password,
        firstName: firstName,
        lastName: lastName,
        email: email
      }),
    });

    const json = await res.json();
    if (json.status === "success") {  // Check for successful registration
      sessionStorage.setItem('username', json.userName);  // Store username
      setOpen(false);
      window.location.href = window.location.origin;  // Redirect to homepage
    } else if (json.error === "Already Registered") {
      alert("The user with the same username is already registered.");
      window.location.href = window.location.origin;  // Redirect after error
    } else {
      alert("Registration failed: " + json.message);  // Handle other errors
    }
  };

  if (!open) {
    window.location.href = "/";  // Redirect to homepage if modal is closed
  }

  return (
    <div className="register_container" style={{ width: "50%" }}>
      <div className="header" style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>
        <span className="text" style={{ flexGrow: "1" }}>SignUp</span> 
        <div style={{ display: "flex", flexDirection: "row", justifySelf: "end", alignSelf: "start" }}>
          <a href="/" onClick={() => { setOpen(false); }} style={{ justifyContent: "space-between", alignItems: "flex-end" }}>
            <img style={{ width: "1cm" }} src={close_icon} alt="X" />
          </a>
        </div>
        <hr />
      </div>
      <form onSubmit={register}>
        <div className="inputs">
          <div className="input">
            <img src={user_icon} className="img_icon" alt='Username' />
            <input type="text" name="username" placeholder="Username" className="input_field" onChange={(e) => setUserName(e.target.value)} />
          </div>
          <div>
            <img src={user_icon} className="img_icon" alt='First Name' />
            <input type="text" name="first_name" placeholder="First Name" className="input_field" onChange={(e) => setFirstName(e.target.value)} />
          </div>
          <div>
            <img src={user_icon} className="img_icon" alt='Last Name' />
            <input type="text" name="last_name" placeholder="Last Name" className="input_field" onChange={(e) => setLastName(e.target.value)} />
          </div>
          <div>
            <img src={email_icon} className="img_icon" alt='Email' />
            <input type="email" name="email" placeholder="Email" className="input_field" onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="input">
            <img src={password_icon} className="img_icon" alt='password' />
            <input name="password" type="password" placeholder="Password" className="input_field" onChange={(e) => setPassword(e.target.value)} />
          </div>
        </div>
        <div className="submit_panel">
          <input className="submit" type="submit" value="Register" />
        </div>
      </form>
    </div>
  );
}

export default Register;
