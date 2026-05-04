import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import MonitoringWidget from "../components/MonitoringWidget";
import LogsWidget from "../components/LogsWidget";
import MLPredictionWidget from "../components/MLPredictionWidget";
import ServiceStatusWidget from "../components/ServiceStatusWidget";
import AutomationWidget from "../components/AutomationWidget";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./AdminDashboard.css";

const AdminDashboard = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [theme, setTheme] = useState(""); // "", "glass", "cyberpunk"
  const navigate = useNavigate();

  useEffect(() => {
    document.title = "OPTIWEB";
    toast.success("Dashboard Loaded", { autoClose: 2000, theme: darkMode ? "dark" : "light" });
  }, []);

  const handleToggleDarkMode = () => {
    setDarkMode((prev) => {
      const newMode = !prev;
      document.body.style.backgroundColor = newMode ? "#1e293b" : "#fff";
      document.body.style.color = newMode ? "#fff" : "#000";
      return newMode;
    });
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className={`admin-dashboard ${darkMode ? "dark-mode" : "light-mode"} ${theme}`}>
      {/* Sidebar Navigation */}
      <aside className="sidebar-nav">
        <div className="nav-icons">
          <Link to="/home" title="Home">
            <img src="/icons/home.png" alt="Home" width={20} />
          </Link>
          <Link to="/admin-dashboard" title="Admin">
            <img src="/icons/admin.png" alt="Admin" width={20} />
          </Link>
          <Link to="/login" title="Login">
            <img src="/icons/login.png" alt="Login" width={20} />
          </Link>
        </div>
        <div className="theme-selector">
          <select onChange={(e) => setTheme(e.target.value)}>
            <option value="">Default</option>
            <option value="glass">Glass</option>
            <option value="cyberpunk">Cyberpunk</option>
          </select>
        </div>
      </aside>

      {/* Toast Notifications */}
      <ToastContainer />

      {/* Top Navbar */}
      <div className="navbar">
        <h1 className="dashboard-title">
          <img src="/icons/opti.png" alt="Admin Icon" width={100} style={{ verticalAlign: "middle", marginRight: "8px" }} />
          Admin Dashboard
        </h1>
        <div className="button-group">
          <button onClick={handleToggleDarkMode}>
            <img
              src={darkMode ? "/icons/sun.png" : "/icons/moon.png"}
              alt="Theme Toggle"
              width={18}
              style={{ marginRight: "6px", verticalAlign: "middle" }}
            />
            {darkMode ? "Light Mode" : "Dark Mode"}
          </button>
          <button className="logout-btn" onClick={handleLogout}>
            <img
              src="/icons/logout.png"
              alt="Logout"
              width={18}
              style={{ marginRight: "6px", verticalAlign: "middle" }}
            />
            Logout
          </button>
        </div>
      </div>

      {/* Mini Status Bar */}
      <div className="mini-stats">
        <img
          src="/icons/correct.png"
          alt="Operational"
          width={26}
          style={{ marginRight: "6px", verticalAlign: "middle" }}
        />
        All Services Operational
      </div>

      {/* First Row */}
      <div className="widgets-grid top-row fade-in">
        <MonitoringWidget />
        <MLPredictionWidget />
        <ServiceStatusWidget />
      </div>

      {/* Second Row */}
      <div className="widgets-grid center-row fade-in">
        <LogsWidget />
        <AutomationWidget />
      </div>
    </div>
  );
};

export default AdminDashboard;
