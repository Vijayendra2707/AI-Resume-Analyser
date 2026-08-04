import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("email", email);
      formData.append("password", password);

      const res = await axios.get(
          `${API_URL}signup`,
        formData
      );

      alert(res.data.message || "Account created successfully!");
      navigate("/login");
    } catch (err) {
      const errorMsg =
        err.response?.data?.detail ||
        "Registration failed. Try again.";

      alert(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrap">
      <div className="auth-left">
        <div className="auth-badge">Create Your Account</div>

        <h1 className="auth-title">
          Start screening<br />
          with AI.
        </h1>

        <p className="auth-sub">
          Create your recruiter account and get instant candidate
          fitment scoring, smart skill gap analysis, and PDF reports.
        </p>
      </div>

      <div className="auth-right">
        <div className="auth-card">
          <h2>Create Account 🚀</h2>
          <p>Join AI Screener Pro</p>

          <form onSubmit={handleSignup}>
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

            <div className="input-group">
              <label className="label">Confirm Password</label>
              <input
                className="input"
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>

            <button
              className="primary-btn"
              type="submit"
              disabled={loading}
              style={{ opacity: loading ? 0.7 : 1 }}
            >
              {loading ? "Creating..." : "Register"}
            </button>
          </form>

          <p style={{ marginTop: 20, marginBottom: 0 }}>
            Already have an account?{" "}
            <a
              href="/login"
              style={{
                color: "#60a5fa",
                fontWeight: 600
              }}
            >
              Login
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Signup;