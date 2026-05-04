import './LogsWidget.css';
import React, { useEffect, useState } from "react";
import api from "../services/api";

const LogsWidget = () => {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedLogs, setSelectedLogs] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedServer, setSelectedServer] = useState("");

  const fetchMetrics = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("Unauthorized: Please log in.");
        setLoading(false);
        return;
      }

      const response = await api.get("/api/auth/metrics/", {
        headers: { Authorization: `Token ${token}` },
      });

      if (response.data.length > 0) {
        setMetrics(response.data);
        setError("");
      } else {
        setError("No metrics available.");
      }

      setLoading(false);
    } catch (err) {
      console.error("Error fetching metrics:", err);
      setError("Failed to fetch metrics");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleRefresh = () => {
    setLoading(true);
    fetchMetrics();
  };

  const openLogModal = (serverId, logString) => {
    const parsedLogs = JSON.parse(logString);
    setSelectedLogs(parsedLogs);
    setSelectedServer(serverId);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedLogs([]);
    setSelectedServer("");
  };

  return (
    <div className="monitoring-widget">
      <div className="header">
        <h2 className="heading-title">Logs Monitoring</h2>
        <button onClick={handleRefresh}>Refresh</button>
      </div>

      {loading ? (
        <p className="status loading">Loading logs...</p>
      ) : error ? (
        <p className="status error">{error}</p>
      ) : (
        <div className="metrics-container">
          {metrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <h3 className="server-label">Server: {metric.server_id}</h3>
              <button
                className="view-logs-btn"
                onClick={() => openLogModal(metric.server_id, metric.logs)}
              >
                View Logs
              </button>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Logs for {selectedServer}</h3>
              <button className="close-btn" onClick={closeModal}>✖</button>
            </div>
            <div className="modal-body">
              <ul>
                {selectedLogs.map((log, idx) => (
                  <li key={idx}>{log}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LogsWidget;
