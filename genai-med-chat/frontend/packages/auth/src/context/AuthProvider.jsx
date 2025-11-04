import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient, setItem, getItem, removeItem } from '@genai-med-chat/shared';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkUser = async () => {
      const token = getItem('token');
      if (token) {
        try {
          const userData = await apiClient.get('/auth/me');
          setUser(userData);
        } catch (error) {
          removeItem('token');
        }
      }
      setLoading(false);
    };

    checkUser();
  }, []);

  const login = async (credentials) => {
    const { token, user } = await apiClient.post('/auth/login', credentials);
    setItem('token', token);
    setUser(user);
    return user;
  };

  const register = async (userData) => {
    const { token, user } = await apiClient.post('/auth/register', userData);
    setItem('token', token);
    setUser(user);
    return user;
  };

  const logout = () => {
    removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;