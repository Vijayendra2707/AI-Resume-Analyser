import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import "./styles.css";

import Login from "./Login";
import Signup from "./Signup";
import Home from "./Home";
import Dashboard from "./Dashboard";
import History from "./History";
import Navbar from "./Navbar";

function App() {
  const isAuthenticated = !!localStorage.getItem("token");

  return (
    <Router>
      {isAuthenticated && <Navbar />}

      <Routes>
        <Route
          path="/"
          element={isAuthenticated ? <Home /> : <Navigate to="/login" />}
        />

        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />

        <Route
          path="/history"
          element={isAuthenticated ? <History /> : <Navigate to="/login" />}
        />

        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;