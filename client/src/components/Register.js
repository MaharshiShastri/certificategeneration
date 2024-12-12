import React, { useState } from 'react';
import { register } from '../api';

const Register = () => {
    const [formData, setFormData] = useState({ name: '', email: '', password: '', role: '' });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await register(formData);
            alert(response.data.message);
        } catch (error) {
            alert(error.response.data.error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="name" placeholder="Name" onChange={handleChange} />
            <input type="email" name="email" placeholder="Email" onChange={handleChange} />
            <input type="password" name="password" placeholder="Password" onChange={handleChange} />
            <select name="role" onChange={handleChange}>
                <option value="">Select Role</option>
                <option value="service-provider">Service Provider</option>
                <option value="customer">Customer</option>
            </select>
            <button type="submit">Register</button>
        </form>
    );
};

export default Register;
