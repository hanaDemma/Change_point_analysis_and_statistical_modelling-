import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import debounce from 'lodash.debounce';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    ComposedChart, Area, Bar, ScatterChart, Scatter, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';
import { Container, Row, Col, Button } from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { addDays, subDays } from 'date-fns';

const EconomicChart = React.memo(({ data }) => (
    <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="Date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="Price" stroke="#8884d8" />
        </LineChart>
    </ResponsiveContainer>
));

const EconomicAnalysis = () => {
    const [econData, setEconData] = useState([]);
    const [loading, setLoading] = useState(true);

    // Set default start and end dates
    const [startDate, setStartDate] = useState(new Date("1987-06-10T00:00:00Z"));
    const [endDate, setEndDate] = useState(new Date("1987-07-30T00:00:00Z"));
    
    // Set date interval for each click (e.g., 30 days)
    const dateInterval = 30;

    const fetchData = async () => {
        try {
            setLoading(true);
            const response = await axios.get('https://backend-brent-oil-latest-1.onrender.com/api/econ_data', {
                params: {
                    start_date: startDate ? startDate.toISOString().split('T')[0] : null,
                    end_date: endDate ? endDate.toISOString().split('T')[0] : null,
                    page: 1,
                    limit: 50
                }
            });
            setEconData(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const debouncedFetchData = useCallback(debounce(fetchData, 500), [startDate, endDate]);

    useEffect(() => {
        debouncedFetchData();
    }, [startDate, endDate, debouncedFetchData]);

    // Adjust the start and end dates when clicking the previous or next buttons
    const handlePrevious = () => {
        setStartDate(prevDate => subDays(prevDate || new Date(), dateInterval));
        setEndDate(prevDate => subDays(prevDate || new Date(), dateInterval));
    };

    const handleNext = () => {
        setStartDate(prevDate => addDays(prevDate || new Date(), dateInterval));
        setEndDate(prevDate => addDays(prevDate || new Date(), dateInterval));
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    // Calculate radar chart data
    const radarChartData = [
        { subject: 'GDP', A: econData.reduce((acc, curr) => acc + (curr.GDP || 0), 0) / econData.length || 0, fullMark: 150 },
        { subject: 'Unemployment', A: econData.reduce((acc, curr) => acc + (curr.Unemployment || 0), 0) / econData.length || 0, fullMark: 150 },
        { subject: 'Inflation', A: econData.reduce((acc, curr) => acc + (curr.Inflation || 0), 0) / econData.length || 0, fullMark: 150 },
    ];

    return (
        <Container>
            <h1>Economic Analysis</h1>
            <Row>
                <Col md={6}>
                    <h4>Date Range</h4>
                    <DatePicker
                        selected={startDate}
                        onChange={date => setStartDate(date)}
                        selectsStart
                        startDate={startDate}
                        endDate={endDate}
                        placeholderText="Start Date"
                    />
                    <DatePicker
                        selected={endDate}
                        onChange={date => setEndDate(date)}
                        selectsEnd
                        startDate={startDate}
                        endDate={endDate}
                        placeholderText="End Date"
                    />
                </Col>
                <Col md={6} className="d-flex align-items-center">
                    <Button onClick={handlePrevious} variant="primary" className="mr-2">&lt; Previous</Button>
                    <Button onClick={handleNext} variant="primary">Next &gt;</Button>
                </Col>
            </Row>

            <Row className="mt-4">
                <Col md={6}>
                    <h2>Oil Prices Over Time</h2>
                    <EconomicChart data={econData} />
                </Col>
                <Col md={6}>
                    <h2>GDP and Unemployment Comparison</h2>
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
                    <h2>Scatter Plot: Oil Prices vs. Inflation</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <ScatterChart>
                            <CartesianGrid />
                            <XAxis dataKey="Price" name="Oil Price" unit="$" />
                            <YAxis dataKey="Inflation" name="Inflation Rate" unit="%" />
                            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                            <Scatter name="Data Points" data={econData} fill="#8884d8" />
                        </ScatterChart>
                    </ResponsiveContainer>
                </Col>
            </Row>

            <Row className="mt-4">
                <Col md={6}>
                    <h2>Radar Chart: Economic Indicators Comparison</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <RadarChart outerRadius={90} data={radarChartData}>
                            <PolarGrid />
                            <PolarAngleAxis dataKey="subject" />
                            <PolarRadiusAxis angle={30} domain={[0, 150]} />
                            <Radar name="Current" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                            <Tooltip />
                        </RadarChart>
                    </ResponsiveContainer>
                </Col>
            </Row>
        </Container>
    );
};

export default EconomicAnalysis;
