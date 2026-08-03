import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const role = localStorage.getItem("role");
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
    window.location.reload();
  };

  if (!token) return null;

  return (
    <nav className="navbar">
      <div className="nav-inner">
        <div className="brand" onClick={() => navigate("/")}>
          AI Screener Pro
        </div>

        <div className="nav-links">
          <Link to="/" className="nav-link">
            Upload
          </Link>

          <Link to="/dashboard" className="nav-link">
            Dashboard
          </Link>

          <Link to="/history" className="nav-link">
            {role === "admin" ? "Recruiter History" : "My Results"}
          </Link>

          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;