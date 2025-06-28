import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TrendingUp, 
  Users, 
  DollarSign, 
  PieChart,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
  Database
} from 'lucide-react';
import { Bar, Pie, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

interface DashboardData {
  summary: any;
  risk_distribution: any[];
  rm_performance: any[];
  charts: any;
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:8000/api/v1/analytics/portfolio-summary');
      setData(response.data);
    } catch (error: any) {
      setError(error.response?.data?.error || 'Failed to fetch dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return `₹${(amount / 10000000).toFixed(1)}Cr`;
  };

  const formatNumber = (num: number) => {
    return num.toLocaleString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {error}
        <button 
          onClick={fetchDashboardData}
          className="ml-4 text-red-600 hover:text-red-800 underline"
        >
          Retry
        </button>
      </div>
    );
  }

  const summary = data?.summary || {};
  const riskDistribution = data?.risk_distribution || [];
  const rmPerformance = data?.rm_performance || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Portfolio Dashboard</h1>
        <p className="text-blue-100">
          Comprehensive overview of wealth portfolios for high net worth individuals
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Users className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Total Clients</h3>
              <p className="text-3xl font-bold text-gray-900">
                {formatNumber(summary.total_clients || 0)}
              </p>
              <p className="text-sm text-gray-500">
                {summary.film_stars || 0} Film Stars, {summary.sports_personalities || 0} Sports
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <DollarSign className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Total AUM</h3>
              <p className="text-3xl font-bold text-gray-900">
                {formatCurrency(summary.total_aum || 0)}
              </p>
              <div className="flex items-center text-sm text-green-600">
                <ArrowUpRight className="h-4 w-4 mr-1" />
                <span>Assets Under Management</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Avg Portfolio</h3>
              <p className="text-3xl font-bold text-gray-900">
                {formatCurrency(summary.avg_portfolio_value || 0)}
              </p>
              <p className="text-sm text-gray-500">Per client average</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Activity className="h-8 w-8 text-orange-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Risk Spread</h3>
              <p className="text-3xl font-bold text-gray-900">
                {riskDistribution.length}
              </p>
              <p className="text-sm text-gray-500">Risk categories</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Portfolio Distribution by Risk Appetite</h3>
          {riskDistribution.length > 0 && (
            <div className="h-64">
              <Pie
                data={{
                  labels: riskDistribution.map(item => item._id),
                  datasets: [{
                    data: riskDistribution.map(item => item.total_value / 10000000),
                    backgroundColor: [
                      'rgba(239, 68, 68, 0.8)',   // Red for Aggressive
                      'rgba(59, 130, 246, 0.8)',  // Blue for Moderate  
                      'rgba(34, 197, 94, 0.8)',   // Green for Conservative
                    ],
                    borderColor: [
                      'rgba(239, 68, 68, 1)',
                      'rgba(59, 130, 246, 1)',
                      'rgba(34, 197, 94, 1)',
                    ],
                    borderWidth: 2
                  }]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom',
                    },
                    tooltip: {
                      callbacks: {
                        label: function(context) {
                          return `${context.label}: ₹${context.parsed}Cr`;
                        }
                      }
                    }
                  }
                }}
              />
            </div>
          )}
        </div>

        {/* RM Performance Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Assets Under Management by RM</h3>
          {rmPerformance.length > 0 && (
            <div className="h-64">
              <Bar
                data={{
                  labels: rmPerformance.map(rm => rm.manager_name),
                  datasets: [{
                    label: 'AUM (₹ Crores)',
                    data: rmPerformance.map(rm => rm.total_aum / 10000000),
                    backgroundColor: 'rgba(59, 130, 246, 0.6)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 1
                  }]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                    tooltip: {
                      callbacks: {
                        label: function(context) {
                          return `AUM: ₹${context.parsed.y}Cr`;
                        }
                      }
                    }
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: 'AUM (₹ Crores)'
                      }
                    }
                  }
                }}
              />
            </div>
          )}
        </div>
      </div>

      {/* Risk Distribution Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Risk Distribution Details</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk Appetite
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Client Count
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Percentage
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {riskDistribution.map((item, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className={`h-3 w-3 rounded-full mr-3 ${
                        item._id === 'Aggressive' ? 'bg-red-500' :
                        item._id === 'Moderate' ? 'bg-blue-500' : 'bg-green-500'
                      }`}></div>
                      <span className="text-sm font-medium text-gray-900">
                        {item._id}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.count}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatCurrency(item.total_value)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {((item.total_value / summary.total_aum) * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button 
            onClick={fetchDashboardData}
            className="flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Database className="h-5 w-5 mr-2" />
            Refresh Data
          </button>
          <button className="flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
            <TrendingUp className="h-5 w-5 mr-2" />
            Generate Report
          </button>
          <button className="flex items-center justify-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
            <PieChart className="h-5 w-5 mr-2" />
            View Analytics
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
