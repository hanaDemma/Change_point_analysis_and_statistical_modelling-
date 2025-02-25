import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    AreaChart, Area, BarChart, Bar, ComposedChart, ReferenceLine
} from 'recharts';
import { Dropdown, Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

function Dashboard() {
    const [econData, setEconData] = useState([]);
    const [techData, setTechData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedEvent, setSelectedEvent] = useState('All');
    const [filteredData, setFilteredData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const econResponse = await axios.get('http://127.0.0.1:5000/api/econ_data');
                const techResponse = await axios.get('http://127.0.0.1:5000/api/tech_data');
                
                setEconData(Array.isArray(econResponse.data) ? econResponse.data : []);
                setTechData(Array.isArray(techResponse.data) ? techResponse.data : []);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        const applyFilter = () => {
            if (selectedEvent === 'All') {
                setFilteredData(econData);
            } else {
                setFilteredData(econData.filter(data => data.Event === selectedEvent));
            }
        };
        applyFilter();
    }, [selectedEvent, econData]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (!econData.length && !techData.length) {
        return <p>No data available</p>;
    }

    return (
        <Container>
            <h1>Brent Oil Price Analysis Dashboard</h1>
            <Dropdown>
                <Dropdown.Toggle variant="success" id="dropdown-basic">
                    Filter by Event: {selectedEvent}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                    <Dropdown.Item onClick={() => setSelectedEvent('All')}>All</Dropdown.Item>
                    <Dropdown.Item onClick={() => setSelectedEvent('Political')}>Political Events</Dropdown.Item>
                    <Dropdown.Item onClick={() => setSelectedEvent('Economic')}>Economic Events</Dropdown.Item>
                    <Dropdown.Item onClick={() => setSelectedEvent('OPEC')}>OPEC Decisions</Dropdown.Item>
                </Dropdown.Menu>
            </Dropdown>

            <Row className="mt-4">
                <Col md={6}>
                    <h2>Brent Oil Prices Over Time</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={filteredData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="Date" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="Price" stroke="#8884d8" />
                            <ReferenceLine y={filteredData[0]?.Price} label="Initial Price" stroke="red" />
                        </LineChart>
                    </ResponsiveContainer>
                </Col>
                <Col md={6}>
                    <h2>Economic Indicators</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <ComposedChart data={econData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="Date" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Area type="monotone" dataKey="GDP" fill="#8884d8" stroke="#8884d8" />
                            <Bar dataKey="Unemployment" barSize={20} fill="#82ca9d" />
                        </ComposedChart>
                    </ResponsiveContainer>
                </Col>
            </Row>

            <Row className="mt-4">
                <Col md={6}>
                    <h2>Technological Data Comparison</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <AreaChart data={techData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="Unnamed: 0" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Area type="monotone" dataKey="Natural_Gas_Value" fill="#ffc658" stroke="#ffc658" />
                            <Area type="monotone" dataKey="value" fill="#82ca9d" stroke="#82ca9d" />
                        </AreaChart>
                    </ResponsiveContainer>
                </Col>
                <Col md={6}>
                    <h2>Price Changes Analysis</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={econData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="Date" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="price_diff" fill="#ff7300" />
                        </BarChart>
                    </ResponsiveContainer>
                </Col>
            </Row>

            <Row className="mt-4">
                <Col md={12}>
                    <h2>Correlation Matrix (Placeholder)</h2>
                    {/* Placeholder for a heatmap or correlation matrix implementation */}
                    <p>Implement a heatmap here using a library like react-heatmap-grid for visualizing correlations between variables.</p>
                </Col>
            </Row>
        </Container>
    );
}

export default Dashboard;