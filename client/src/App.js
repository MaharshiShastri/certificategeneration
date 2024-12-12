import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

const App = () => {
    const [role, setRole] = useState(null);

    const handleLogin = (userRole) => {
        setRole(userRole);
    };

    return (
        <Router>
            <Routes>
                {/* Public Routes */}
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login onLogin={handleLogin} />} />

                {/* Protected Route */}
                <Route
                    path="/dashboard"
                    element={role ? <Dashboard role={role} /> : <Navigate to="/login" />}
                />

                {/* Default Route */}
                <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
};

export default App;
