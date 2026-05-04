// App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import AdminDashboard from "./pages/AdminDashboard";
import UserDashboard from "./pages/UserDashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AgentDownload from "./pages/AgentDownload";

const App = () => {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/admin-dashboard" element={<AdminDashboard />} />
                <Route path="/user-dashboard" element={<UserDashboard />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/Home" element={<Home />} />
                <Route path="/" element={<Home />} />
                <Route path="/dashboard" element={<AdminDashboard />} />
                <Route path="/agent-download" element={<AgentDownload />} />
            </Routes>
        </Router>
    );
};

export default App;
