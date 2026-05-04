import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  return (
    <nav className="main-navbar">
      <ul className="nav-list">
        <li>
          <Link to="/home">
            <img src="/icons/home.png" alt="Home" className="nav-icon" />
            Home
          </Link>
        </li>
        <li>
          <Link to="/admin-dashboard">
            <img src="/icons/admin.png" alt="Dashboard" className="nav-icon" />
            Dashboard
          </Link>
        </li>
        <li>
          <Link to="/login">
            <img src="/icons/login.png" alt="Login" className="nav-icon" />
            Login
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
