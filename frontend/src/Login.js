import React, { useState } from 'react';
import axios from 'axios';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:5000/api/login', {
        username, password
      });
      localStorage.setItem('token', res.data.token);
      onLogin();
    } catch (err) {
      setError('Invalid username or password!');
    }
  };

  return (
    <div style={{
      background: '#0a0a0a', minHeight: '100vh',
      display: 'flex', justifyContent: 'center', alignItems: 'center'
    }}>
      <div style={{
        background: '#1a1a1a', padding: '40px',
        borderRadius: '15px', border: '1px solid #00ff88',
        width: '350px', textAlign: 'center'
      }}>
        <h1 style={{ color: '#00ff88', marginBottom: '10px' }}>🛡️ SIEM</h1>
        <p style={{ color: '#888', marginBottom: '30px' }}>Security Dashboard Login</p>

        {error && <p style={{ color: '#ff4444', marginBottom: '15px' }}>{error}</p>}

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            width: '100%', padding: '12px', marginBottom: '15px',
            background: '#0a0a0a', border: '1px solid #333',
            borderRadius: '8px', color: 'white', fontSize: '16px',
            boxSizing: 'border-box'
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: '100%', padding: '12px', marginBottom: '20px',
            background: '#0a0a0a', border: '1px solid #333',
            borderRadius: '8px', color: 'white', fontSize: '16px',
            boxSizing: 'border-box'
          }}
        />

        <button
          onClick={handleLogin}
          style={{
            width: '100%', padding: '12px',
            background: '#00ff88', color: 'black',
            border: 'none', borderRadius: '8px',
            fontSize: '16px', fontWeight: 'bold', cursor: 'pointer'
          }}
        >
          LOGIN
        </button>

        <p style={{ color: '#555', marginTop: '20px', fontSize: '12px' }}>
          Default: admin / admin123
        </p>
      </div>
    </div>
  );
}

export default Login;