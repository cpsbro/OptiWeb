import React, { useEffect, useState } from "react";
import api from "../services/api";
import "./MLPredictionWidget.css";

const MLPredictionWidget = () => {
  const [failureRisk, setFailureRisk] = useState(null);
  const [reasons, setReasons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);

  const fetchPrediction = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setError(" Unauthorized: Please log in.");
        setLoading(false);
        return;
      }

      const metricsResponse = await api.get("/api/auth/metrics/", {
        headers: { Authorization: `Token ${token}` },
      });

      if (metricsResponse.data.length === 0) {
        setError(" No metrics data available for prediction.");
        setLoading(false);
        return;
      }

      const latestMetrics = metricsResponse.data[0];

      const mlPayload = {
        server_id: latestMetrics.server_id,
        cpu_usage: latestMetrics.cpu_usage,
        memory_usage: latestMetrics.memory_usage,
        disk_usage: latestMetrics.disk_usage,
        uptime: latestMetrics.uptime,
        web_service_status: latestMetrics.web_service_status || "{}",
        db_service_status: latestMetrics.db_service_status || "{}",
        logs: latestMetrics.logs || "[]",
      };

      const predictionResponse = await api.post("/api/ml/predict/", mlPayload, {
        headers: { Authorization: `Token ${token}` },
      });

      setFailureRisk(predictionResponse.data.failure_risk);
      setReasons(predictionResponse.data.reasons);
      setLoading(false);
    } catch (err) {
      console.error("Prediction API Error:", err);
      setError(" Failed to fetch AI predictions.");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrediction();
    const interval = setInterval(fetchPrediction, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="ml-widget-container">
      <div className="ml-header">
        <h3>AI Failure Prediction</h3>
        <button onClick={fetchPrediction}>Refresh</button>
      </div>

      {loading && <p className="ml-status loading">Loading predictions...</p>}
      {error && <p className="ml-status error">{error}</p>}

      {!loading && !error && (
        <div className={`ml-card ${failureRisk ? "high" : "low"}`}>
          <p className="ml-risk">
            <strong>Failure Risk:</strong>{" "}
            <span className={failureRisk ? "risk-high" : "risk-low"}>
              {failureRisk ? "HIGH RISK" : "LOW RISK"}
            </span>
          </p>
          <button className="ml-reasons-btn" onClick={() => setShowModal(true)}>
            View Reasons
          </button>
        </div>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>AI Risk Reasons</h3>
              <button className="close-btn" onClick={() => setShowModal(false)}>✖</button>
            </div>
            <div className="modal-body">
              {reasons.length > 0 ? (
                <ul>
                  {reasons.map((reason, idx) => (
                    <li key={idx}>{reason}</li>
                  ))}
                </ul>
              ) : (
                <p>No reasons provided.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MLPredictionWidget;
