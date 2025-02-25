// src/components/Dashboard.js
import React from 'react';
import { Container } from 'react-bootstrap';
import '../styles.css';


const Dashboard = () => {
    return (
        <Container>
            <h1>Welcome to the Dashboard</h1>
            <p>Select a section from the navigation bar to view the analyses.</p>
        </Container>
    );
};

export default Dashboard;