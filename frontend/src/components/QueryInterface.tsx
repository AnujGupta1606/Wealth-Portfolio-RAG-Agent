import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, MessageSquare, Bot, User, Loader, BarChart3, Download } from 'lucide-react';
import { Bar, Pie } from 'react-chartjs-2';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  chart_data?: any;
}

const QueryInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentQuery, setCurrentQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sampleQueries = [
    "What are the top five portfolios of our wealth members?",
    "Give me the breakup of portfolio values per relationship manager.",
    "Tell me the top relationship managers in my firm",
    "Which clients are the highest holders of RELIANCE stock?",
    "Show me the risk distribution across all portfolios",
    "What is the average portfolio size for film stars vs sports personalities?",
    "Which stocks have the highest concentration across all portfolios?",
    "Show me recent transaction activity for high-value trades"
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQuery.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: currentQuery,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentQuery('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/v1/query/ask', {
        question: currentQuery,
        conversation_id: conversationId,
        include_charts: true
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.data.answer,
        timestamp: new Date(),
        chart_data: response.data.chart_data
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      if (response.data.conversation_id && !conversationId) {
        setConversationId(response.data.conversation_id);
      }

    } catch (error: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error.response?.data?.detail || 'Please try again later.'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSampleQuery = (query: string) => {
    setCurrentQuery(query);
  };

  const renderChart = (chartData: any) => {
    if (!chartData) return null;

    const chartProps = {
      data: chartData.data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom' as const,
          },
          title: {
            display: true,
            text: chartData.title
          },
          tooltip: {
            callbacks: {
              label: function(context: any) {
                if (chartData.type === 'pie') {
                  return `${context.label}: ₹${context.parsed}Cr`;
                }
                return `${context.dataset.label}: ₹${context.parsed.y}Cr`;
              }
            }
          }
        },
        ...(chartData.type === 'bar' && {
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Value (₹ Crores)'
              }
            }
          }
        })
      }
    };

    return (
      <div className="mt-4 bg-gray-50 p-4 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-gray-700 flex items-center">
            <BarChart3 className="h-4 w-4 mr-1" />
            {chartData.title}
          </h4>
          <button className="text-gray-500 hover:text-gray-700">
            <Download className="h-4 w-4" />
          </button>
        </div>
        <div className="h-64">
          {chartData.type === 'pie' ? 
            <Pie {...chartProps} /> : 
            <Bar {...chartProps} />
          }
        </div>
      </div>
    );
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center space-x-3">
          <MessageSquare className="h-8 w-8 text-blue-600" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Natural Language Query Interface</h1>
            <p className="text-gray-600">Ask questions about portfolios, clients, and transactions in plain English</p>
          </div>
        </div>
      </div>

      {/* Sample Queries */}
      {messages.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Try these sample queries:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {sampleQueries.map((query, index) => (
              <button
                key={index}
                onClick={() => handleSampleQuery(query)}
                className="text-left p-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors border border-blue-200"
              >
                <span className="text-blue-700 text-sm">{query}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 bg-white rounded-lg shadow-sm overflow-hidden flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-12">
              <Bot className="h-12 w-12 mx-auto text-gray-400 mb-4" />
              <p className="text-lg">Start a conversation with your wealth data</p>
              <p className="text-sm">Ask questions about portfolios, clients, or market analysis</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex space-x-3 max-w-3xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                  <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
                    message.type === 'user' ? 'bg-blue-600' : 'bg-gray-600'
                  }`}>
                    {message.type === 'user' ? 
                      <User className="h-4 w-4 text-white" /> : 
                      <Bot className="h-4 w-4 text-white" />
                    }
                  </div>
                  <div className={`flex-1 ${message.type === 'user' ? 'text-right' : ''}`}>
                    <div className={`inline-block px-4 py-2 rounded-lg ${
                      message.type === 'user' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-100 text-gray-900'
                    }`}>
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                    {message.chart_data && renderChart(message.chart_data)}
                    <p className={`text-xs text-gray-500 mt-1 ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
                      {formatTime(message.timestamp)}
                    </p>
                  </div>
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex justify-start">
              <div className="flex space-x-3">
                <div className="flex-shrink-0 h-8 w-8 rounded-full bg-gray-600 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-white" />
                </div>
                <div className="flex-1">
                  <div className="inline-block px-4 py-2 rounded-lg bg-gray-100 text-gray-900">
                    <div className="flex items-center space-x-2">
                      <Loader className="h-4 w-4 animate-spin" />
                      <span>Analyzing your query...</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="border-t border-gray-200 p-4">
          <form onSubmit={handleSubmit} className="flex space-x-4">
            <div className="flex-1">
              <input
                type="text"
                value={currentQuery}
                onChange={(e) => setCurrentQuery(e.target.value)}
                placeholder="Ask about portfolios, clients, transactions, or market analysis..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={loading}
              />
            </div>
            <button
              type="submit"
              disabled={loading || !currentQuery.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <Loader className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default QueryInterface;
