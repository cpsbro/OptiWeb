import React, { useEffect, useState } from "react";
import "./AgentDownload.css"; // import custom CSS

const AgentDownload = () => {
  const [userToken, setUserToken] = useState("");
  const [serverIP, setServerIP] = useState("");

  useEffect(() => {
    setUserToken(localStorage.getItem("userToken") || "YOUR_API_TOKEN");
    setServerIP(localStorage.getItem("serverIP") || "YOUR_SERVER_IP");
  }, []);

  return (
    <div className="agent-container">
      <div className="agent-box">
        <h2 className="agent-title">
          Download and Install the OptiWeb Monitoring Agent
        </h2>
        <p className="agent-description">
          Follow these steps to set up the monitoring agent on your server:
        </p>

        <div className="agent-step">
          <h3>Download the Agent</h3>
          <p>use below link to download Agent:</p>
          <pre>https://drive.google.com/file/d/18_Y-Kni6ashoz2RPZWaswcICz7xN4X6B/view?usp=drive_link</pre>
        </div>

        <div className="agent-step">
          <h3>Install Required Python Dependencies</h3>
          <p>Install necessary libraries:</p>
          <pre>pip install psutil requests</pre>
          <p>Optionally, create a virtual environment:</p>
          <pre>
            python3 -m venv optiweb_env
            <br />
            source optiweb_env/bin/activate
          </pre>
        </div>

        <div className="agent-step">
          <h3>Create Configuration File</h3>
          <p>Create a file named <code>config.json</code> in the same folder as <code>agent.py</code>:</p>
          <pre>nano config.json</pre>
          <p>Paste this content:</p>
          <pre>
{`{
  "backend_api": "http://203.143.13.21:8000/api/auth/metrics/",
  "web_server_ip": "${serverIP}",
  "token": "${userToken}"
}`}
          </pre>
          <p className="highlight">Replace values with your actual <strong>server IP</strong> and <strong>API token</strong> if not pre-filled.</p>
        </div>

        <div className="agent-step">
          <h3>Run the Agent (Foreground)</h3>
          <p>Start the agent to view logs live:</p>
          <pre>python3 agent.py</pre>
          <p>The agent sends data every 60 seconds.</p>
          <p>To run in the background:</p>
          <pre>nohup python3 agent.py &gt; agent.log 2&gt;&amp;1 &amp;</pre>
          <p>Check logs later:</p>
          <pre>tail -f agent.log</pre>
        </div>

        <div className="agent-step">
          <h3>Verify in Dashboard</h3>
          <p>Your server metrics should appear under:</p>
          <ul>
            <li>Monitoring</li>
            <li>ML Prediction</li>
            <li>Logs</li>
            <li>Service Status</li>
          </ul>
        </div>

        <div className="agent-help">
          <h3>Need Help?</h3>
          <p>Email: <a href="mailto:chameerahetti1998@gmail.com">chameerahetti1998@gmail.com</a></p>
          <p>Or check the dashboard for FAQ/help section.</p>
        </div>
      </div>
    </div>
  );
};

export default AgentDownload;
