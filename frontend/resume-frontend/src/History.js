import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

function History() {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem("token");
          const res = await axios.get(
          `${API_URL}/history`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        setRecords(res.data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="page">
      <section className="page-section">
        <div className="container">
          <h1 className="hero-title">Analysis History</h1>
          <p className="hero-sub">
            Review previously screened candidates and reports.
          </p>

          <div className="white-card table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Candidate</th>
                  <th>Fitment Score</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th>Report</th>
                </tr>
              </thead>

              <tbody>
                {records.length > 0 ? (
                  records.map((r) => (
                    <tr key={r.id}>
                      <td>
                        <b>{r.candidate_name}</b>
                      </td>

                      <td>
                        <b>{r.score}%</b>
                      </td>

                      <td>
                        <span
                          className={`status ${
                            r.shortlisted ? "green" : "red"
                          }`}
                        >
                          {r.shortlisted
                            ? "Recommended"
                            : "Rejected"}
                        </span>
                      </td>

                      <td>
                        {new Date(
                          r.timestamp
                        ).toLocaleDateString()}
                      </td>

                      <td>
                        <a
                          href={r.report_url}
                          target="_blank"
                          rel="noreferrer"
                          style={{
                            color: "#3b82f6",
                            fontWeight: 600
                          }}
                        >
                          View PDF
                        </a>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan="5"
                      style={{
                        textAlign: "center",
                        color: "#64748b",
                        padding: 40
                      }}
                    >
                      No history found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}

export default History;