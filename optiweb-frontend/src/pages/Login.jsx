import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Login.css"; // Import CSS file

const Login = () => {
  const [formData, setFormData] = useState({ web_server_ip: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/api/auth/login/", formData, {
        headers: { "Content-Type": "application/json" },
      });

      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
        navigate("/dashboard");
      } else {
        alert("Login failed. Please check your credentials.");
      }
    } catch (error) {
      alert("Login failed. Please check your credentials.");
      console.error("Login error:", error.response?.data || error.message);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Login</h2>
        <form onSubmit={handleSubmit} className="login-form">
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
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
