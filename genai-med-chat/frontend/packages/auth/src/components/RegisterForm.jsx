import React, { useState } from 'react';
import { Button, Input, Card, ErrorMessage } from '@genai-med-chat/shared';
import { validateEmail, validatePassword, validateName } from '@genai-med-chat/shared';

const RegisterForm = ({ onRegister, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    const validationErrors = {};
    const nameError = validateName(formData.name);
    if (nameError) validationErrors.name = nameError;

    if (!validateEmail(formData.email)) {
      validationErrors.email = 'Invalid email address';
    }

    const passwordError = validatePassword(formData.password);
    if (passwordError) validationErrors.password = passwordError;

    if (formData.password !== formData.confirmPassword) {
      validationErrors.confirmPassword = 'Passwords do not match';
    }

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    try {
      await onRegister({ name: formData.name, email: formData.email, password: formData.password });
    } catch (err) {
      setErrors({ form: err.message || 'Registration failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Register" subtitle="Create your GenAI Medical Chat account">
      <form onSubmit={handleSubmit} className="space-y-4">
        {errors.form && <ErrorMessage message={errors.form} />}
        
        <Input
          type="text"
          name="name"
          placeholder="Enter your full name"
          value={formData.name}
          onChange={handleChange}
          label="Full Name"
          error={errors.name}
          required
        />
        
        <Input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={handleChange}
          label="Email"
          error={errors.email}
          required
        />
        
        <Input
          type="password"
          name="password"
          placeholder="Create a password"
          value={formData.password}
          onChange={handleChange}
          label="Password"
          error={errors.password}
          required
        />
        
        <Input
          type="password"
          name="confirmPassword"
          placeholder="Confirm your password"
          value={formData.confirmPassword}
          onChange={handleChange}
          label="Confirm Password"
          error={errors.confirmPassword}
          required
        />
        
        <div className="flex space-x-4">
          <Button type="submit" disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </Button>
          
          <Button 
            type="button" 
            variant="secondary" 
            onClick={onSwitchToLogin}
            disabled={loading}
          >
            Login
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default RegisterForm;