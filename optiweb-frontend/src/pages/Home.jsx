import React from "react";
import { Link } from "react-router-dom";
import {
  Button,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
} from "@mui/material";
import "./Home.css";

const features = [
  {
    title: "Web Sever Monitoring",
    description:
      "Track server health, database performance, and network activity in real-time.",
  },
  {
    title: "Predictive Maintenance",
    description:
      "AI-powered insights to predict and prevent bugs and issues before they occur.",
  },
  {
    title: "Automation",
    description:
      "Automate bug resolution and system recovery with advanced algorithms.",
  },
  {
    title: "User-Friendly Dashboard",
    description:
      "Intuitive and responsive dashboards for seamless management.",
  },
];

const Home = () => {
  return (
    <div className="home-container">
      {/* Welcome Section */}
      <div className="welcome-section">
        <Typography variant="h2" className="welcome-title">
          Welcome to OptiWeb Zone
        </Typography>
        <Typography variant="h6" className="welcome-subtitle">
          Your one-stop solution for web server monitoring, predictive maintenance,
          and automation.
        </Typography>
        <Grid container justifyContent="center" spacing={2}>
          <Grid item>
            <Link to="/register">
              <Button variant="contained" className="green-btn">
                Register
              </Button>
            </Link>
          </Grid>
          <Grid item>
            <Link to="/login">
              <Button variant="contained" className="green-btn">
                Login
              </Button>
            </Link>
          </Grid>
        </Grid>
      </div>

      {/* Features Section */}
      <Container maxWidth="lg" className="features-section">
        <Typography variant="h4" className="features-title">
          OptiWeb Features
        </Typography>
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card className="feature-card">
                <CardContent>
                  <Typography variant="h6" className="feature-title">
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" className="feature-description">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Why Choose Section */}
      <div className="why-choose-section">
        <Typography variant="h4" className="why-choose-title">
          Why Choose OptiWeb?
        </Typography>
        <Typography variant="h6" className="why-choose-subtitle">
          Cutting-edge technology designed to optimize, monitor, and automate
          your online systems.
        </Typography>
        <Grid container justifyContent="center" spacing={2}>
          <Grid item>
            <Link to="/contact">
              <Button variant="contained" className="green-btn">
                Contact Us
              </Button>
            </Link>
          </Grid>
        </Grid>
      </div>
    </div>
  );
};

export default Home;
