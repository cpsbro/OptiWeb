import React, { useState, useEffect } from "react";
import api from "../services/api";
import "./ServiceStatusWidget.css";

const ServiceStatusWidget = () => {
  const [webServices, setWebServices] = useState([]);
  const [dbServices, setDbServices] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchServiceStatus = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) return;

      const response = await api.get("/api/auth/metrics/", {
        headers: { Authorization: `Token ${token}` },
      });

      if (Array.isArray(response.data) && response.data.length > 0) {
        const metric = response.data[0];

        const parsedWebServices = metric.web_service_status ? JSON.parse(metric.web_service_status) : {};
        const parsedDbServices = metric.db_service_status ? JSON.parse(metric.db_service_status) : {};

        const installedWebServices = Object.entries(parsedWebServices)
          .map(([service, status]) => ({ name: service, status }))
          .filter(service => service.status === "active" || service.status === "inactive");

        const installedDbServices = Object.entries(parsedDbServices)
          .map(([service, status]) => ({ name: service, status }))
          .filter(service => service.status === "active" || service.status === "inactive");

        setWebServices(installedWebServices);
        setDbServices(installedDbServices);
      }

      setLoading(false);
    } catch (error) {
      console.error("Error fetching service status:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServiceStatus();
    const interval = setInterval(fetchServiceStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="service-status-widget">
      <div className="service-header">
        <h3 className="widget-title">Service Status</h3>
      </div>

      {loading ? (
        <p className="status loading">Loading...</p>
      ) : (
        <div className="services-list">
          {webServices.length > 0 && (
            <div className="service-block">
              <h4>Web Services</h4>
              <ul>
                {webServices.map((service, index) => (
                  <li key={index}>
                    <span className={`service-name ${service.status}`}>
                      {service.name}
                    </span>
                    <span className={`status-badge ${service.status}`}>
                      {service.status.toUpperCase()}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {dbServices.length > 0 && (
            <div className="service-block">
              <h4>Database Services</h4>
              <ul>
                {dbServices.map((service, index) => (
                  <li key={index}>
                    <span className={`service-name ${service.status}`}>
                      {service.name}
                    </span>
                    <span className={`status-badge ${service.status}`}>
                      {service.status.toUpperCase()}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {webServices.length === 0 && dbServices.length === 0 && (
            <p>No Installed Services Found</p>
          )}
        </div>
      )}
    </div>
  );
};

export default ServiceStatusWidget;
