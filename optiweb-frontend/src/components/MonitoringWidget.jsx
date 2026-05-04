import "./MonitoringWidget.css";
import React, { useEffect, useState } from "react";
import api from "../services/api";

const MonitoringWidget = () => {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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

      if (Array.isArray(response.data) && response.data.length > 0) {
        setMetrics(response.data);
        setError("");
        setLoading(false);
      } else {
        setError("No metrics available.");
        setLoading(false);
      }
    } catch (err) {
      console.error("Error fetching metrics:", err);
      setError("Failed to fetch metrics.");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 10000);
    return () => clearInterval(interval);
  }, []);

  const getColor = (value) => {
    if (value >= 80) return "red";
    if (value >= 50) return "orange";
    return "green";
  };

  const renderCircle = (label, value) => {
    const radius = 35;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (value / 100) * circumference;
    const color = getColor(value);

    return (
      <div className="circle-box" key={label}>
        <svg className="progress-circle">
          <circle className="bg" cx="40" cy="40" r={radius} />
          <circle
            className={`fg ${color}`}
            cx="40"
            cy="40"
            r={radius}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
          <text x="40" y="46" textAnchor="middle" className="circle-text">
            {value}%
          </text>
        </svg>
        <div className="circle-label">{label}</div>
      </div>
    );
  };

  return (
    <div className="monitoring-widget">
      <div className="header">
        <h2 className="heading-title">Metrics Monitoring</h2>
        <button onClick={fetchMetrics}>Refresh</button>
      </div>

      {loading ? (
        <p className="status loading">Loading...</p>
      ) : error ? (
        <p className="status error">{error}</p>
      ) : (
        <div className="metrics-container">
          {metrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <h3 className="server-label">Server: {metric.server_id}</h3>
              <div className="circles-row">
                {renderCircle("CPU", Math.floor(metric.cpu_usage))}
                {renderCircle("RAM", Math.floor(metric.memory_usage))}
                {renderCircle("Disk", Math.floor(metric.disk_usage))}
              </div>

              <div className="uptime-graph">
                <div
                  className="uptime-bar"
                  style={{ width: `${Math.min(metric.uptime / 100, 100)}%` }}
                >
                  {Math.floor(metric.uptime / 3600)} hrs
                </div>
              </div>

              <div className="timestamp-box">
                <span className="timestamp-label">Timestamp:</span>{" "}
                <span className="timestamp-value">
                  {new Date(metric.timestamp).toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MonitoringWidget;
