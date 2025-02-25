import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Row, Col, Container } from 'react-bootstrap';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    BarChart, Bar, PieChart, Pie, Cell, ScatterChart, Scatter,
    RadarChart, Radar, LineChart, Line, ComposedChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';

import '../styles.css';

const TechnologicalAnalysis = () => {
    const [techData, setTechData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('https://backend-brent-oil-latest-1.onrender.com/api/tech_data');
                setTechData(Array.isArray(response.data) ? response.data : []);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <Container>
            <h1>Technological Analysis</h1>
            <Row>
                <Col md={6}>
                    <h2>Natural Gas vs Oil Prices (Scatter Plot)</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <ScatterChart>
                            <CartesianGrid />
                            <XAxis dataKey="Natural_Gas_Value" name="Natural Gas Value" unit="$" />
                            <YAxis dataKey="Oil_Price" name="Oil Price" unit="$" />
                            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                            <Scatter name="Data Points" data={techData} fill="#8884d8" />
                        </ScatterChart>
                    </ResponsiveContainer>
                </Col>
                <Col md={6}>
                    <h2>Technological Sector Contribution (Pie Chart)</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={[
                                    { name: 'Natural Gas', value: techData.reduce((acc, item) => acc + item.Natural_Gas_Value, 0) },
                                    { name: 'Oil', value: techData.reduce((acc, item) => acc + item.Oil_Price, 0) },
                                ]}
                                cx="50%"
                                cy="50%"
                                outerRadius={100}
                                fill="#82ca9d"
                                dataKey="value"
                            >
                                {[{ name: 'Natural Gas' }, { name: 'Oil' }].map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={`#${Math.floor(Math.random() * 16777215).toString(16)}`} />
                                ))}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </Col>
            </Row>

            <Row className="mt-4">
                <Col md={6}>
                    <h2>Bar Chart: Oil Price Changes</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={techData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="year" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="Oil_Price" fill="#ff7300" />
                            <Bar dataKey="Oil_Price_Diff" fill="#82ca9d" />
                        </BarChart>
                    </ResponsiveContainer>
                </Col>
                <Col md={6}>
                    <h2>Radar Chart: Sector Performance</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <RadarChart outerRadius={90} data={[
                            { subject: 'Natural Gas', A: techData[0]?.Natural_Gas_Value || 0, B: techData[0]?.Natural_Gas_Rolling || 0, fullMark: 15 },
                            { subject: 'Oil', A: techData[0]?.Oil_Price || 0, B: techData[0]?.Oil_Price_Diff || 0, fullMark: 15 },
                        ]}>
                            <PolarGrid />
                            <PolarAngleAxis dataKey="subject" />
                            <PolarRadiusAxis angle={30} domain={[0, 15]} />
                            <Radar name="Current" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                            <Radar name="Previous" dataKey="B" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                            <Tooltip />
                        </RadarChart>
                    </ResponsiveContainer>
                </Col>
            </Row>
        </Container>
    );
};

export default TechnologicalAnalysis;
