import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import '../styles.css';


function Dashboard() {
    const [econData, setEconData] = useState([]);
    const [techData, setTechData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const econResponse = await axios.get('http://127.0.0.1:5000/api/econ_data');
                const techResponse = await axios.get('http://127.0.0.1:5000/api/tech_data');
                
                // console.log("Econ Data:", econResponse.data); // Log econ data
                console.log("Tech Data:", techResponse.data); // Log tech data
                
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

    if (loading) {
        return <p>Loading...</p>;
    }

    if (!econData.length && !techData.length) {
        return <p>No data available</p>;
    }

    return (
        <div>
            <h2>Economic Data</h2>
            <LineChart
                width={500}
                height={300}
                data={econData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="Date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="Price" stroke="#8884d8" />
                <Line type="monotone" dataKey="Unemployment" stroke="#82ca9d" />
            </LineChart>

            <h2>Technological Data</h2>
            <LineChart
                width={500}
                height={300}
                data={techData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="Unnamed: 0" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="Natural_Gas_Value" stroke="#8884d8" />
                <Line type="monotone" dataKey="value" stroke="#82ca9d" />
            </LineChart>
        </div>
    );
}

export default Dashboard;
