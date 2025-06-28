import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { TrendingUp, Shield, Database } from 'lucide-react';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    try {
      await login(username, password);
      // Navigate to dashboard after successful login
      navigate('/');
    } catch (error: any) {
      setError(error.response?.data?.error || 'Login failed');
    }
  };

  const demoCredentials = [
    { username: 'admin', password: 'admin123', role: 'Administrator' },
    { username: 'manager', password: 'manager123', role: 'Manager' },
    { username: 'analyst', password: 'analyst123', role: 'Analyst' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-cyan-600 flex items-center justify-center p-4">
      <div className="max-w-6xl w-full grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        {/* Left side - Feature showcase */}
        <div className="text-white space-y-8">
          <div className="space-y-4">
            <h1 className="text-5xl font-bold">
              Wealth Portfolio
              <span className="text-cyan-300"> RAG Agent</span>
            </h1>
            <p className="text-xl text-blue-100">
              Natural Language Cross-Platform Data Query System for High Net Worth Portfolio Management
            </p>
          </div>

          <div className="space-y-6">
            <div className="flex items-center space-x-4">
              <div className="bg-blue-700/50 p-3 rounded-lg">
                <TrendingUp className="h-6 w-6 text-cyan-300" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">Advanced Analytics</h3>
                <p className="text-blue-200">AI-powered insights for 100+ crore portfolios</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="bg-blue-700/50 p-3 rounded-lg">
                <Database className="h-6 w-6 text-cyan-300" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">Multi-Source Data</h3>
                <p className="text-blue-200">MongoDB + MySQL integration with LangChain</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="bg-blue-700/50 p-3 rounded-lg">
                <Shield className="h-6 w-6 text-cyan-300" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">Enterprise Security</h3>
                <p className="text-blue-200">Secure access for film stars & sports personalities</p>
              </div>
            </div>
          </div>

          <div className="bg-blue-800/30 p-6 rounded-lg">
            <h4 className="text-lg font-semibold mb-3">Business Scenario</h4>
            <p className="text-blue-100">
              Managing wealth portfolios for film stars and sports personalities with 100+ crores invested. 
              Client profiles in MongoDB, transaction data in MySQL, powered by LangChain RAG for natural language queries.
            </p>
          </div>
        </div>

        {/* Right side - Login form */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Welcome Back</h2>
            <p className="text-gray-600 mt-2">Sign in to your wealth management dashboard</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your username"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your password"
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="mt-8">
            <h3 className="text-sm font-medium text-gray-700 mb-4">Demo Credentials:</h3>
            <div className="space-y-2">
              {demoCredentials.map((cred, index) => (
                <div 
                  key={index}
                  className="flex items-center justify-between bg-gray-50 p-3 rounded-lg cursor-pointer hover:bg-gray-100"
                  onClick={() => {
                    setUsername(cred.username);
                    setPassword(cred.password);
                  }}
                >
                  <div>
                    <span className="font-medium text-sm">{cred.username}</span>
                    <span className="text-gray-500 text-xs ml-2">({cred.role})</span>
                  </div>
                  <span className="text-xs text-gray-400">Click to use</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
