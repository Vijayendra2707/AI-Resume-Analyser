import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

function Home() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem("result");
  }, []);

  const handleUpload = async () => {
    if (!file || !jd) {
      alert("Please provide both a resume and a job description.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("jd_text", jd);

    try {
      const token = localStorage.getItem("token");

      const res = await axios.get(
          `${API_URL}/analyze_resume`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      localStorage.setItem("result", JSON.stringify(res.data));
      navigate("/dashboard");
    } catch (err) {
      alert("Analysis failed. Check backend server.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page">
        <div
          className="container"
          style={{
            minHeight: "80vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
          }}
        >
          <div
            className="glass-card"
            style={{
              width: "100%",
              maxWidth: 650,
              textAlign: "center"
            }}
          >
            <h1 style={{ marginBottom: 15 }}>
              🚀 AI is analyzing your profile...
            </h1>

            <p
              style={{
                color: "#94a3b8",
                lineHeight: 1.8
              }}
            >
              Extracting skills, measuring similarity,
              checking missing concepts, and generating
              recommendations.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <section className="page-section">
        <div className="container">
          <h1 className="hero-title">Resume Screening</h1>
          <p className="hero-sub">
            Upload candidate resume + paste job description for AI evaluation.
          </p>

          <div
            className="glass-card"
            style={{
              maxWidth: 850,
              margin: "auto"
            }}
          >
            <label className="label">Job Description</label>

            <textarea
              className="textarea"
              placeholder="Paste complete job requirements here..."
              value={jd}
              onChange={(e) => setJd(e.target.value)}
            />

            <label className="label">Upload Resume</label>

            <label className="upload-box">
              <div style={{ fontSize: 45, marginBottom: 10 }}>📄</div>

              <h3 style={{ marginBottom: 8 }}>
                {file ? file.name : "Choose Resume File"}
              </h3>

              <p style={{ color: "#94a3b8" }}>
                PDF / DOCX supported
              </p>

              <input
                type="file"
                hidden
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>

            <button
              className="primary-btn"
              onClick={handleUpload}
            >
              Analyze Candidate →
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;