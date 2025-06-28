import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Database, RefreshCw, Upload, Download, AlertTriangle, CheckCircle } from 'lucide-react';

interface DataStats {
  clients: { clients: any[]; count: number };
  transactions: { transactions: any[]; count: number };
  holdings: { holdings: any[]; count: number };
  relationship_managers: { relationship_managers: any[]; count: number };
}

const DataManagement: React.FC = () => {
  const [stats, setStats] = useState<DataStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [initializingData, setInitializingData] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchDataStats();
  }, []);

  const fetchDataStats = async () => {
    try {
      setLoading(true);
      const [clientsRes, transactionsRes, holdingsRes, rmsRes] = await Promise.all([
        axios.get('http://localhost:8000/api/v1/data/clients'),
        axios.get('http://localhost:8000/api/v1/data/transactions'),
        axios.get('http://localhost:8000/api/v1/data/portfolio-holdings'),
        axios.get('http://localhost:8000/api/v1/data/relationship-managers')
      ]);

      setStats({
        clients: clientsRes.data,
        transactions: transactionsRes.data,
        holdings: holdingsRes.data,
        relationship_managers: rmsRes.data
      });
    } catch (error: any) {
      setError(error.response?.data?.error || 'Failed to fetch data stats');
    } finally {
      setLoading(false);
    }
  };

  const initializeSampleData = async () => {
    try {
      setInitializingData(true);
      await axios.post('http://localhost:8000/api/v1/data/initialize-sample-data');
      await fetchDataStats(); // Refresh data after initialization
    } catch (error: any) {
      setError(error.response?.data?.error || 'Failed to initialize sample data');
    } finally {
      setInitializingData(false);
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview' },
    { id: 'clients', name: 'Clients' },
    { id: 'transactions', name: 'Transactions' },
    { id: 'holdings', name: 'Holdings' },
    { id: 'managers', name: 'Managers' }
  ];

  const formatCurrency = (amount: number) => {
    return `₹${(amount / 10000000).toFixed(1)}Cr`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-blue-600 rounded-xl p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Data Management</h1>
        <p className="text-green-100">
          Monitor and manage your wealth portfolio data across MongoDB and MySQL
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center">
          <AlertTriangle className="h-5 w-5 mr-2" />
          {error}
          <button 
            onClick={fetchDataStats}
            className="ml-4 text-red-600 hover:text-red-800 underline"
          >
            Retry
          </button>
        </div>
      )}

      {/* Data Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Database className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Clients</h3>
              <p className="text-3xl font-bold text-gray-900">
                {stats?.clients?.count || 0}
              </p>
              <p className="text-sm text-gray-500">MongoDB Collection</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Database className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Transactions</h3>
              <p className="text-3xl font-bold text-gray-900">
                {stats?.transactions?.count || 0}
              </p>
              <p className="text-sm text-gray-500">MySQL Table</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Database className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Holdings</h3>
              <p className="text-3xl font-bold text-gray-900">
                {stats?.holdings?.count || 0}
              </p>
              <p className="text-sm text-gray-500">Portfolio Holdings</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Database className="h-8 w-8 text-orange-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Managers</h3>
              <p className="text-3xl font-bold text-gray-900">
                {stats?.relationship_managers?.count || 0}
              </p>
              <p className="text-sm text-gray-500">Relationship Managers</p>
            </div>
          </div>
        </div>
      </div>

      {/* Data Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Operations</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button 
            onClick={fetchDataStats}
            className="flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            disabled={loading}
          >
            <RefreshCw className={`h-5 w-5 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh Data
          </button>
          
          <button 
            onClick={initializeSampleData}
            className="flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            disabled={initializingData}
          >
            <Upload className={`h-5 w-5 mr-2 ${initializingData ? 'animate-spin' : ''}`} />
            {initializingData ? 'Initializing...' : 'Initialize Sample Data'}
          </button>
          
          <button className="flex items-center justify-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
            <Download className="h-5 w-5 mr-2" />
            Export Data
          </button>
          
          <button className="flex items-center justify-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
            <CheckCircle className="h-5 w-5 mr-2" />
            Validate Data
          </button>
        </div>
      </div>

      {/* Data Tables */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h4 className="text-lg font-semibold text-blue-900 mb-2">MongoDB Status</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span>Clients Collection:</span>
                      <span className="font-medium">{stats?.clients?.count || 0} records</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Holdings Collection:</span>
                      <span className="font-medium">{stats?.holdings?.count || 0} records</span>
                    </div>
                    <div className="flex items-center">
                      <div className="h-3 w-3 bg-green-400 rounded-full mr-2"></div>
                      <span className="text-green-700">Connected</span>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 p-6 rounded-lg">
                  <h4 className="text-lg font-semibold text-green-900 mb-2">MySQL Status</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span>Transactions Table:</span>
                      <span className="font-medium">{stats?.transactions?.count || 0} records</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Last Transaction:</span>
                      <span className="font-medium">
                        {stats?.transactions?.transactions?.[0]?.transaction_date 
                          ? formatDate(stats.transactions.transactions[0].transaction_date)
                          : 'N/A'
                        }
                      </span>
                    </div>
                    <div className="flex items-center">
                      <div className="h-3 w-3 bg-green-400 rounded-full mr-2"></div>
                      <span className="text-green-700">Connected</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Data Health Summary</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {stats ? '✓' : '✗'}
                    </div>
                    <div className="text-sm text-gray-600">Data Connectivity</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {(stats?.clients?.count || 0) > 0 ? '✓' : '✗'}
                    </div>
                    <div className="text-sm text-gray-600">Client Data</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {(stats?.transactions?.count || 0) > 0 ? '✓' : '✗'}
                    </div>
                    <div className="text-sm text-gray-600">Transaction Data</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Clients Tab */}
          {activeTab === 'clients' && (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Client ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Portfolio Value
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Risk Appetite
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      RM
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {stats?.clients?.clients?.slice(0, 10).map((client) => (
                    <tr key={client.client_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {client.client_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {client.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          client.type === 'Film Star' 
                            ? 'bg-purple-100 text-purple-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}>
                          {client.type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {formatCurrency(client.total_portfolio_value)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          client.risk_appetite === 'Aggressive' 
                            ? 'bg-red-100 text-red-800'
                            : client.risk_appetite === 'Moderate'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {client.risk_appetite}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {client.relationship_manager_name}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Transactions Tab */}
          {activeTab === 'transactions' && (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Client ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Stock
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Quantity
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Amount
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {stats?.transactions?.transactions?.slice(0, 10).map((transaction, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {formatDate(transaction.transaction_date)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {transaction.client_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          transaction.transaction_type === 'BUY' 
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {transaction.transaction_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {transaction.stock_symbol}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {transaction.quantity?.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ₹{transaction.total_amount?.toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DataManagement;
