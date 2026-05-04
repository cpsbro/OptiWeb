import React, { useEffect, useState } from "react";
import api from "../services/api";
import "./AutomationWidget.css";

const AutomationWidget = () => {
  const [automationLogs, setAutomationLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fixing, setFixing] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const fetchAutomationLogs = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) return;

      const response = await api.get("/api/automation/logs/", {
        headers: { Authorization: `Token ${token}` },
      });

      if (response.data.length > 0) {
        setAutomationLogs(response.data);
      } else {
        setAutomationLogs([]);
      }
      setLoading(false);
    } catch (error) {
      console.error("Error fetching automation logs:", error);
      setLoading(false);
    }
  };

  const handleManualFix = async () => {
    setFixing(true);
    setStatusMessage("");

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setStatusMessage("Unauthorized: Please log in.");
        setFixing(false);
        return;
      }

      const response = await api.post(
        "/api/automation/fix_issue/",
        {},
        {
          headers: { Authorization: `Token ${token}` },
        }
      );

      if (response.status === 200) {
        setStatusMessage(" Auto-fix triggered successfully.");
        fetchAutomationLogs();
      } else {
        setStatusMessage(" Auto-fix failed.");
      }
    } catch (error) {
      console.error("Error during manual fix:", error);
      setStatusMessage(" Error running auto-fix.");
    } finally {
      setFixing(false);
    }
  };

  useEffect(() => {
    fetchAutomationLogs();
    const interval = setInterval(fetchAutomationLogs, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="automation-widget">
      <div className="automation-header">
        <h3 className="automation-title">Automated Issue Resolution</h3>
        <button
          className={`auto-fix-btn ${fixing ? "fixing" : ""}`}
          onClick={handleManualFix}
          disabled={fixing}
        >
          {fixing ? "Running Fix..." : "Run Auto Fix"}
        </button>
      </div>

      {statusMessage && <p className="status-message">{statusMessage}</p>}

      <div className="automation-logs">
        {loading ? (
          <p className="status loading">Loading logs...</p>
        ) : automationLogs.length > 0 ? (
          <ul>
            {automationLogs.map((log, idx) => (
              <li key={idx}>
                <span className="log-time">{log.timestamp}</span>
                <span className="log-text">
                   {log.service_name}: {log.fix_result}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="status">No automated fixes applied recently.</p>
        )}
      </div>
    </div>
  );
};

export default AutomationWidget;
