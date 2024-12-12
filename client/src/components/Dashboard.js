import React from 'react';

const Dashboard = ({ role }) => {
    return (
        <div>
            <h1>Welcome to the {role === 'service-provider' ? 'Service Provider' : 'Customer'} Dashboard</h1>
        </div>
    );
};

export default Dashboard;
