// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CustomNavbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import EconomicAnalysis from './components/EconomicAnalysis';
import TechnologicalAnalysis from './components/TechnologicalAnalysis';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles.css';

const App = () => {
    return (
        <Router>
            <CustomNavbar />
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/economic-analysis" element={<EconomicAnalysis />} />
                <Route path="/technological-analysis" element={<TechnologicalAnalysis />} />
            </Routes>
        </Router>
    );
};

export default App;