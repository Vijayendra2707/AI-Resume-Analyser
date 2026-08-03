import React, { useEffect, useState } from "react";
import { getHistory, getAnalytics } from "./api";

function Admin() {
  const [history, setHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    getHistory().then(setHistory);
    getAnalytics().then(setAnalytics);
  }, []);

  return (
    <div style={{ padding: 40, backgroundColor: "#f9fafb", minHeight: "100vh" }}>
      <h1>Admin Dashboard</h1>
      
      {/* Stats Cards */}
      <div style={{ display: "flex", gap: 20, marginBottom: 40 }}>
        <div style={cardStyle}>
          <h3>Total Analyzed</h3>
          <p style={{ fontSize: 32, fontWeight: "bold" }}>{history.length}</p>
        </div>
        <div style={cardStyle}>
          <h3>Top Missing Skill</h3>
          <p style={{ fontSize: 24, color: "red" }}>
            {analytics?.top_missing_skills[0]?.[0] || "N/A"}
          </p>
        </div>
      </div>

      <h3>Analysis History</h3>
      <table style={{ width: "100%", background: "white", borderRadius: 8, borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#3b82f6", color: "white" }}>
            <th style={thStyle}>Candidate</th>
            <th style={thStyle}>Score</th>
            <th style={thStyle}>Status</th>
            <th style={thStyle}>Confidence</th>
            <th style={thStyle}>Date</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h) => (
            <tr key={h.id} style={{ borderBottom: "1px solid #ddd" }}>
              <td style={tdStyle}>{h.candidate_name}</td>
              <td style={tdStyle}>{h.score}%</td>
              <td style={{ ...tdStyle, color: h.shortlisted ? "green" : "red", fontWeight: "bold" }}>
                {h.shortlisted ? "SHORTLISTED" : "REJECTED"}
              </td>
              <td style={tdStyle}>{h.confidence}%</td>
              <td style={tdStyle}>{new Date(h.timestamp).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const cardStyle = { padding: 20, background: "white", borderRadius: 12, flex: 1, boxShadow: "0 2px 10px rgba(0,0,0,0.1)" };
const thStyle = { padding: 15, textAlign: "left" };
const tdStyle = { padding: 15 };

export default Admin;