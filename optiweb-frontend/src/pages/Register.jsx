import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Register.css"; // Import CSS file

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    web_server_ip: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [userToken, setUserToken] = useState("");
  const [showPopup, setShowPopup] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/api/auth/register/", formData);
      const { token } = response.data;

      // Store token and web server IP in local storage
      localStorage.setItem("userToken", token);
      localStorage.setItem("serverIP", formData.web_server_ip);

      // Show success message and token
      setMessage(response.data.message);
      setUserToken(token);
      setShowPopup(true);
    } catch (error) {
      setMessage("Registration failed.");
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2>Register</h2>
        <form onSubmit={handleSubmit} className="register-form">
          <input
            type="text"
            name="username"
            placeholder="Username"
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="web_server_ip"
            placeholder="Web Server IP"
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            required
          />
          <button type="submit">Register</button>
        </form>
      </div>

      {/* Success Popup */}
      {showPopup && (
        <div className="popup-overlay">
          <div className="popup">
            <h3>Registration Successful!</h3>
            <p>Your API Token:</p>
            <strong className="token">{userToken}</strong>
            <p>Use this token to authenticate your agent.</p>
            <button onClick={() => navigate("/agent-download")}>
              Download Agent
            </button>
            <button className="close-btn" onClick={() => setShowPopup(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Register;
