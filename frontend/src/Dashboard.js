import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

const fetchData = async () => {
  try {
    const token = localStorage.getItem('token');
    const config = { headers: { Authorization: `Bearer ${token}` }};
    const logsRes = await axios.get('http://localhost:5000/api/logs', config);
    const statsRes = await axios.get('http://localhost:5000/api/stats', config);
    setLogs(logsRes.data);
    setStats(statsRes.data);
  } catch (err) {
    console.log('Error:', err);
  }
};

  const severityColor = (severity) => {
    const colors = {
      'CRITICAL': '#ff4444',
      'HIGH': '#ff8800',
      'MEDIUM': '#ffcc00',
      'LOW': '#00cc44'
    };
    return colors[severity] || '#ffffff';
  };

  return (
    <div style={{ background: '#0a0a0a', minHeight: '100vh', color: 'white', padding: '20px' }}>
      
      <h1 style={{ color: '#00ff88', textAlign: 'center', marginBottom: '30px' }}>
        🛡️ SIEM Security Dashboard
      </h1>

      {/* Stats Cards */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '30px', flexWrap: 'wrap' }}>
        {[
          { label: 'Total Events', value: stats.total_events, color: '#0088ff' },
          { label: 'Critical Alerts', value: stats.critical_alerts, color: '#ff4444' },
          { label: 'Blocked IPs', value: stats.blocked_ips, color: '#ff8800' },
          { label: 'Active Threats', value: stats.active_threats, color: '#cc00ff' }
        ].map((card) => (
          <div key={card.label} style={{
            background: '#1a1a1a',
            border: `1px solid ${card.color}`,
            borderRadius: '10px',
            padding: '20px',
            flex: '1',
            minWidth: '150px',
            textAlign: 'center'
          }}>
            <h2 style={{ color: card.color, fontSize: '2rem', margin: '0' }}>{card.value}</h2>
            <p style={{ color: '#aaa', margin: '5px 0 0 0' }}>{card.label}</p>
          </div>
        ))}
      </div>

      {/* Log Table */}
      <div style={{ background: '#1a1a1a', borderRadius: '10px', padding: '20px', overflowX: 'auto' }}>
        <h3 style={{ color: '#00ff88', marginTop: '0' }}>📋 Live Security Logs</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #333' }}>
              {['ID', 'Time', 'IP Address', 'Event', 'Severity', 'Location'].map(h => (
                <th key={h} style={{ padding: '10px', color: '#888', textAlign: 'left' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} style={{ borderBottom: '1px solid #222' }}>
                <td style={{ padding: '8px', color: '#aaa' }}>#{log.id}</td>
                <td style={{ padding: '8px', color: '#aaa' }}>{log.timestamp}</td>
                <td style={{ padding: '8px', color: '#00aaff' }}>{log.ip_address}</td>
                <td style={{ padding: '8px', color: 'white' }}>{log.event_type}</td>
                <td style={{ padding: '8px' }}>
                  <span style={{
                    background: severityColor(log.severity),
                    color: 'black',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontWeight: 'bold',
                    fontSize: '12px'
                  }}>
                    {log.severity}
                  </span>
                </td>
                <td style={{ padding: '8px', color: '#aaa' }}>{log.location}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;