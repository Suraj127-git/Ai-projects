import React, { useState } from 'react';
import { Button, Input, Card, ErrorMessage } from '@genai-med-chat/shared';

const LoginForm = ({ onLogin, onSwitchToRegister }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await onLogin(formData);
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Login" subtitle="Welcome back to GenAI Medical Chat">
      <form onSubmit={handleSubmit} className="space-y-4">
        <ErrorMessage message={error} />
        
        <Input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={handleChange}
          label="Email"
          required
        />
        
        <Input
          type="password"
          name="password"
          placeholder="Enter your password"
          value={formData.password}
          onChange={handleChange}
          label="Password"
          required
        />
        
        <div className="flex space-x-4">
          <Button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </Button>
          
          <Button 
            type="button" 
            variant="secondary" 
            onClick={onSwitchToRegister}
            disabled={loading}
          >
            Register
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default LoginForm;