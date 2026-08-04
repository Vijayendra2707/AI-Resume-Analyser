import React, { useState } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("username", email);
      formData.append("password", password);

      const res = await axios.post(
          `${API_URL}/login`,
        formData
      );

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.role);

      window.location.href = "/";
    } catch (err) {
      alert("Invalid Credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrap">
      <div className="auth-left">
        <div className="auth-badge">AI Powered Recruitment</div>

        <h1 className="auth-title">
          Hire smarter.<br />
          Screen faster.
        </h1>

        <p className="auth-sub">
          Analyze resumes instantly with AI-driven fitment scoring,
          skill matching, recommendations, and recruiter-ready reports.
        </p>
      </div>

      <div className="auth-right">
        <div className="auth-card">
          <h2>Welcome Back 👋</h2>
          <p>Login to continue your analysis workflow</p>

          <form onSubmit={handleLogin}>
            <div className="input-group">
              <label className="label">Email</label>
              <input
                className="input"
                type="email"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label className="label">Password</label>
              <input
                className="input"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button
              className="primary-btn"
              type="submit"
              disabled={loading}
              style={{ opacity: loading ? 0.7 : 1 }}
            >
              {loading ? "Signing In..." : "Login"}
            </button>
          </form>

          <p style={{ marginTop: 20, marginBottom: 0 }}>
            Don't have an account?{" "}
            <a
              href="/signup"
              style={{
                color: "#60a5fa",
                fontWeight: 600
              }}
            >
              Create one
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;