import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Radar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler
} from "chart.js";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

ChartJS.register(
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler
);

function Dashboard() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const result = JSON.parse(localStorage.getItem("result"));
    if (result) setData(result);
  }, []);

  const handleNewAnalysis = () => {
    localStorage.removeItem("result");
    navigate("/");
  };

  if (!data) {
    return (
      <div className="page">
        <div
          className="container"
          style={{
            minHeight: "70vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
          }}
        >
          <div className="glass-card" style={{ textAlign: "center" }}>
            <h2>No Analysis Data Found</h2>
            <p style={{ color: "#94a3b8", marginTop: 10 }}>
              Upload a resume first.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const getCatPercent = (catName) => {
    const cat = data.categorized_skills?.[catName];
    if (!cat) return 0;

    const total = cat.matched.length + cat.missing.length;
    return total > 0
      ? Math.round((cat.matched.length / total) * 100)
      : 0;
  };

  const radarData = {
    labels: [
      "Tech Skills",
      "Tools",
      "Concepts",
      "Similarity",
      "Confidence"
    ],
    datasets: [
      {
        label: "Match %",
        data: [
          getCatPercent("technical_skills"),
          getCatPercent("tools"),
          getCatPercent("concepts"),
          (data.similarity || 0) * 100,
          data.confidence || 0
        ],
        backgroundColor: "rgba(59,130,246,.2)",
        borderColor: "#3b82f6",
        pointBackgroundColor: "#3b82f6",
        borderWidth: 2
      }
    ]
  };

  const renderBadge = (text, good = true) => (
    <span
      style={{
        padding: "7px 12px",
        borderRadius: 12,
        fontSize: 13,
        fontWeight: 600,
        display: "inline-block",
        background: good
          ? "rgba(16,185,129,.15)"
          : "rgba(239,68,68,.15)",
        color: good ? "#86efac" : "#fca5a5",
        margin: 5
      }}
    >
      {text}
    </span>
  );

  return (
    <div className="page">
      <section className="page-section">
        <div className="container">
          {/* Header */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              gap: 20,
              flexWrap: "wrap",
              marginBottom: 30
            }}
          >
            <div>
              <h1 className="hero-title">Candidate Analysis</h1>
              <p className="hero-sub">{data.candidate_name}</p>
            </div>

            <div style={{ display: "flex", gap: 12 }}>
              <button
              onClick={handleNewAnalysis}
              style={{
                  border: "none",
                  padding: "12px 20px",
                  height: "48px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: "12px",
                  fontSize: "15px",
                  background: "#334155",
                  color: "white",
                  fontWeight: 600
                }}
                          >
                New Analysis
              </button>
              <a
                href={data.report_url}
                target="_blank"
                rel="noreferrer"
                style={{
                  padding: "12px 20px",
                  height: "48px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: "12px",
                  fontSize: "15px",
                  background: "linear-gradient(135deg,#10b981,#059669)",
                  color: "white",
                  fontWeight: 600
                }}
              >
                Download PDF
              </a>
            </div>
          </div>

          {/* Metric cards */}
          <div className="grid-3" style={{ marginBottom: 30 }}>
            <div className="metric-card">
              <div className="metric-title">FITMENT SCORE</div>
              <div className="metric-value">{data.score}%</div>
            </div>

            <div className="metric-card">
              <div className="metric-title">STATUS</div>
              <div className="metric-value" style={{ fontSize: 22 }}>
                {data.shortlisted ? "Recommended" : "Rejected"}
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-title">SIMILARITY</div>
              <div className="metric-value">
                {Math.round((data.similarity || 0) * 100)}%
              </div>
            </div>
          </div>

          {/* Score + radar */}
          <div className="grid-2">
            <div className="white-card">
              <h3 style={{ marginBottom: 25 }}>Overall Score</h3>

              <div style={{ width: 180, margin: "auto" }}>
                <CircularProgressbar
                  value={data.score}
                  text={`${data.score}%`}
                  styles={buildStyles({
                    pathColor: "#3b82f6",
                    textColor: "#111827",
                    trailColor: "#e5e7eb"
                  })}
                />
              </div>

              <div style={{ marginTop: 25 }}>
                <p>
                  <b>Context Match:</b>{" "}
                  {data.breakdown?.similarity_score}/40
                </p>

                <p style={{ marginTop: 8 }}>
                  <b>Skill Match:</b>{" "}
                  {data.breakdown?.skill_score}/60
                </p>
              </div>
            </div>

            <div className="white-card">
              <h3 style={{ marginBottom: 20 }}>
                Skill Visualization
              </h3>

              <div style={{ height: 320 }}>
                <Radar
                  data={radarData}
                  options={{
                    maintainAspectRatio: false,
                    scales: {
                      r: {
                        min: 0,
                        max: 100,
                        ticks: { display: false }
                      }
                    }
                  }}
                />
              </div>
            </div>
          </div>

          {/* AI Analysis */}
          <div
            className="white-card"
            style={{
              marginTop: 30,
              borderLeft: `6px solid ${
                data.shortlisted ? "#10b981" : "#ef4444"
              }`
            }}
          >
            <h3 style={{ marginBottom: 15 }}>
              AI Analysis
            </h3>

            <p
              style={{
                color: "#475569",
                lineHeight: 1.9,
                whiteSpace: "pre-wrap"
              }}
            >
              {data.reasoning}
            </p>

            {data.improvement_suggestion && (
              <div
                style={{
                  marginTop: 20,
                  padding: 18,
                  borderRadius: 16,
                  background: "#fffbeb"
                }}
              >
                <b style={{ color: "#92400e" }}>
                  Career Tip:
                </b>

                <p
                  style={{
                    marginTop: 8,
                    color: "#b45309"
                  }}
                >
                  {data.improvement_suggestion}
                </p>
              </div>
            )}
          </div>

          {/* Skill Breakdown */}
          <div style={{ marginTop: 35 }}>
            <h2 style={{ marginBottom: 20 }}>
              Skill Breakdown
            </h2>

            <div className="grid-3">
              {["technical_skills", "tools", "concepts"].map((cat) => (
                <div
                  className="glass-card"
                  key={cat}
                >
                  <h3
                    style={{
                      marginBottom: 20,
                      textTransform: "capitalize",
                      color: "white"
                    }}
                  >
                    {cat.replace("_", " ")}
                  </h3>

                  <p
                    style={{
                      color: "#86efac",
                      fontWeight: 700,
                      marginBottom: 10
                    }}
                  >
                    MATCHED
                  </p>

                  <div>
                    {data.categorized_skills?.[cat]?.matched?.length
                      ? data.categorized_skills[cat].matched.map((s, i) => (
                          <React.Fragment key={i}>
                            {renderBadge(s, true)}
                          </React.Fragment>
                        ))
                      : "None"}
                  </div>

                  <p
                    style={{
                      color: "#fca5a5",
                      fontWeight: 700,
                      marginTop: 20,
                      marginBottom: 10
                    }}
                  >
                    MISSING
                  </p>

                  <div>
                    {data.categorized_skills?.[cat]?.missing?.length
                      ? data.categorized_skills[cat].missing.map((s, i) => (
                          <React.Fragment key={i}>
                            {renderBadge(s, false)}
                          </React.Fragment>
                        ))
                      : "None"}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Learning Paths */}
          {data.course_links &&
            Object.keys(data.course_links).length > 0 && (
              <div style={{ marginTop: 50, marginBottom: 30 }}>
                <h2
                  style={{
                    marginBottom: 24,
                    fontSize: "30px",
                    fontWeight: 700,
                    color: "white"
                  }}
                >
                  Recommended Learning Paths
                </h2>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "repeat(auto-fit,minmax(240px,320px))",
                    gap: "24px",
                    justifyContent: "center"
                  }}
                >
                  {Object.entries(data.course_links).map(
                    ([skill, links]) => (
                      <div
                        key={skill}
                        className="learn-card"
                        style={{
                          background:
                            "rgba(255,255,255,0.08)",
                          backdropFilter: "blur(18px)",
                          border:
                            "1px solid rgba(255,255,255,0.08)",
                          borderRadius: "22px",
                          padding: "24px",
                          boxShadow:
                            "0 20px 40px rgba(0,0,0,.25)",
                          transition: ".25s"
                        }}
                      >
                        <h3
                          style={{
                            marginBottom: 20,
                            color: "#ffffff",
                            fontSize: "20px",
                            textTransform: "capitalize"
                          }}
                        >
                          {skill}
                        </h3>

                        <div
                          style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "12px"
                          }}
                        >
                          <a
                            href={links.Coursera}
                            target="_blank"
                            rel="noreferrer"
                            style={{
                              padding: "12px 16px",
                              background:
                                "rgba(59,130,246,.15)",
                              borderRadius: "12px",
                              color: "#93c5fd",
                              fontWeight: 600
                            }}
                          >
                            🎓 Coursera Course
                          </a>

                          <a
                            href={links.YouTube}
                            target="_blank"
                            rel="noreferrer"
                            style={{
                              padding: "12px 16px",
                              background:
                                "rgba(239,68,68,.12)",
                              borderRadius: "12px",
                              color: "#fca5a5",
                              fontWeight: 600
                            }}
                          >
                            📺 YouTube Tutorial
                          </a>

                          <a
                            href={links.Udemy}
                            target="_blank"
                            rel="noreferrer"
                            style={{
                              padding: "12px 16px",
                              background:
                                "rgba(139,92,246,.12)",
                              borderRadius: "12px",
                              color: "#c4b5fd",
                              fontWeight: 600
                            }}
                          >
                            🚀 Udemy Specialization
                          </a>
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}
        </div>
      </section>
    </div>
  );
}

export default Dashboard;