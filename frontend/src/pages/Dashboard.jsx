// Dashboard.jsx
import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Download, Copy, RefreshCw, X, Search, AlertTriangle, Clock } from 'lucide-react';

const CATEGORY_COLORS = {
  Essential: '#0ea5a4',
  Analytics: '#4f46e5',
  Advertising: '#fb7185',
  Functional: '#f59e0b',
  Security: '#10b981',
  Necessary: '#0ea5a4',
  Performance: '#8b5cf6',
  Other: '#6b7280'
};

const CookieScanDashboard = ({
  scanResult,
  onRescan = (url) => console.log('Rescan:', url),
  onExportCSV = (sr) => console.log('Export CSV:', sr),
  onCopyJSON = (sr) => console.log('Copy JSON:', sr),
  onCookieClick = (c) => console.log('Cookie clicked:', c)
}) => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCookie, setSelectedCookie] = useState(null);


  // Loading state
  if (!scanResult) {
    return (
      <div className="min-h-screen bg-gray-50 p-4 md:p-8 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
          <p className="text-gray-600 text-lg">Loading scan results...</p>
        </div>
      </div>
    );
  }

  // Ensure cookies array exists
  const cookies = scanResult.cookies || [];
  const summaryByCategory = scanResult.summaryByCategory || {};

  // Convert UTC to IST
  const formatDateIST = (dateString) => {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Invalid Date';
    
    // Convert to IST (UTC + 5:30)
    const istOffset = 5.5 * 60 * 60 * 1000;
    const istDate = new Date(date.getTime() + istOffset);
    
    const year = istDate.getUTCFullYear();
    const month = String(istDate.getUTCMonth() + 1).padStart(2, '0');
    const day = String(istDate.getUTCDate()).padStart(2, '0');
    const hours = String(istDate.getUTCHours()).padStart(2, '0');
    const minutes = String(istDate.getUTCMinutes()).padStart(2, '0');
    const seconds = String(istDate.getUTCSeconds()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds} IST`;
  };

  const filteredCookies = useMemo(() => {
    return cookies.filter(cookie => {
      const matchesCategory = !selectedCategory || cookie.category === selectedCategory;
      const matchesSearch = !searchTerm || 
        (cookie.name && cookie.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (cookie.domain && cookie.domain.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (cookie.vendor && cookie.vendor.toLowerCase().includes(searchTerm.toLowerCase()));
      return matchesCategory && matchesSearch;
    });
  }, [cookies, selectedCategory, searchTerm]);

  const categoryData = Object.entries(summaryByCategory).map(([name, value]) => ({
    name,
    value,
    color: CATEGORY_COLORS[name] || '#6b7280'
  }));

  const handleExportCSV = () => {
    try {
      const headers = ['Name', 'Category', 'Domain', 'Expires', 'Secure', 'HttpOnly', 'Vendor', 'Purpose'];
      const rows = cookies.map(c => [
        c.name || '',
        c.category || '',
        c.domain || '',
        c.expires || 'session',
        c.secure || false,
        c.httpOnly || false,
        c.vendor || '',
        c.purpose || ''
      ]);
      const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cookie-scan-${new Date().getTime()}.csv`;
      a.click();
      URL.revokeObjectURL(url);
      alert('CSV exported successfully!');
    } catch (error) {
      console.error('CSV export error:', error);
      alert('Failed to export CSV');
    }
  };

  const handleCopyJSON = () => {
    try {
      navigator.clipboard.writeText(JSON.stringify(scanResult, null, 2));
      alert('JSON copied to clipboard!');
    } catch (error) {
      console.error('Copy error:', error);
      alert('Failed to copy JSON');
    }
  };

  const formatExpiry = (expires) => {
    if (!expires || expires === 'session') return 'Session';
    
    // If it's a timestamp (number)
    if (typeof expires === 'number') {
      const date = new Date(expires * 1000);
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
    }
    
    // If it's already a date string
    const date = new Date(expires);
    if (isNaN(date.getTime())) return expires;
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Scan Results</h1>
            <p className="text-gray-600 flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Last scanned: {formatDateIST(scanResult.scannedAt)}
            </p>
          </div>
          <div className="flex gap-2 flex-wrap">
            <button 
              onClick={() => onRescan(scanResult.url)} 
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm"
            >
              <RefreshCw className="w-4 h-4" />
              Re-scan
            </button>
            <button 
              onClick={handleExportCSV} 
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </button>
            <button 
              onClick={handleCopyJSON} 
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Copy className="w-4 h-4" />
              Copy JSON
            </button>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="text-center flex-1">
              <div className="text-6xl font-bold text-gray-900 mb-2">{scanResult.totalCookies || cookies.length}</div>
              <div className="text-sm text-gray-600">Cookies (in total)</div>
            </div>
            <div className="flex-1 grid grid-cols-2 gap-x-8 gap-y-3">
              {categoryData.map((cat, idx) => (
                <div key={idx} className="flex items-center gap-3">
                  <div 
                    className="w-3 h-3 rounded-full flex-shrink-0" 
                    style={{ backgroundColor: cat.color }}
                  ></div>
                  <span className="text-sm text-gray-700 flex-1">{cat.name}</span>
                  <span className="text-lg font-bold text-gray-900">{cat.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Cookies by Category</h3>
          {categoryData.length > 0 ? (
            <>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryData} layout="vertical">
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={100} />
                  <Tooltip />
                  <Bar 
                    dataKey="value" 
                    radius={[0, 8, 8, 0]} 
                    onClick={(data) => setSelectedCategory(data.name === selectedCategory ? null : data.name)} 
                    className="cursor-pointer"
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              {selectedCategory && (
                <div className="mt-3 text-sm text-gray-600">
                  Filtered by: <span className="font-semibold">{selectedCategory}</span>
                  <button onClick={() => setSelectedCategory(null)} className="ml-2 text-indigo-600 hover:text-indigo-700">Clear filter</button>
                </div>
              )}
            </>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              No category data available
            </div>
          )}
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input 
                type="text" 
                placeholder="Search cookies..." 
                value={searchTerm} 
                onChange={(e) => setSearchTerm(e.target.value)} 
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" 
              />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200 sticky top-0 z-10">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Cookie</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Domain</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Description</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Duration</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Type</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredCookies.length > 0 ? (
                  filteredCookies.map((cookie, idx) => (
                    <tr key={idx} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button 
                          onClick={() => { setSelectedCookie(cookie); onCookieClick(cookie); }} 
                          className="text-indigo-600 hover:text-indigo-900 font-medium"
                        >
                          {cookie.name || 'Unknown'}
                        </button>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{cookie.domain || 'N/A'}</td>
                      <td className="px-6 py-4 text-sm text-gray-700 max-w-md">
                        {cookie.purpose || 'No description available'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                        {cookie.duration_human || 'Session'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span 
                          className="px-3 py-1 rounded-full text-xs font-semibold text-white" 
                          style={{ backgroundColor: CATEGORY_COLORS[cookie.category] || '#6b7280' }}
                        >
                          {cookie.category || 'Other'}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                      No cookies found matching your filters
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        <AnimatePresence>
          {selectedCookie && (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              exit={{ opacity: 0 }} 
              className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50" 
              onClick={() => setSelectedCookie(null)}
            >
              <motion.div 
                initial={{ scale: 0.9, opacity: 0 }} 
                animate={{ scale: 1, opacity: 1 }} 
                exit={{ scale: 0.9, opacity: 0 }} 
                onClick={(e) => e.stopPropagation()} 
                className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto"
              >
                <div className="p-6 border-b border-gray-200 flex items-center justify-between">
                  <h2 className="text-2xl font-bold text-gray-900">{selectedCookie.name || 'Cookie Details'}</h2>
                  <button 
                    onClick={() => setSelectedCookie(null)} 
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <X className="w-6 h-6" />
                  </button>
                </div>
                <div className="p-6 space-y-4">
                  <div>
                    <div className="text-sm font-semibold text-gray-700 mb-1">Category</div>
                    <span 
                      className="px-3 py-1 rounded-full text-sm font-semibold text-white inline-block" 
                      style={{ backgroundColor: CATEGORY_COLORS[selectedCookie.category] || '#6b7280' }}
                    >
                      {selectedCookie.category || 'Other'}
                    </span>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-700 mb-1">Purpose</div>
                    <p className="text-gray-900">{selectedCookie.purpose || 'No description available'}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-sm font-semibold text-gray-700 mb-1">Domain</div>
                      <p className="text-gray-900">{selectedCookie.domain || 'N/A'}</p>
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-gray-700 mb-1">Vendor</div>
                      <p className="text-gray-900">{selectedCookie.vendor || '—'}</p>
                    </div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-700 mb-2">Security Attributes</div>
                    <div className="flex flex-wrap gap-2">
                      <div className={`px-3 py-1 rounded-lg text-sm font-medium ${selectedCookie.secure ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {selectedCookie.secure ? '✓ Secure' : '✗ Not Secure'}
                      </div>
                      <div className={`px-3 py-1 rounded-lg text-sm font-medium ${selectedCookie.httpOnly ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {selectedCookie.httpOnly ? '✓ HttpOnly' : '✗ Not HttpOnly'}
                      </div>
                    </div>
                  </div>
                  <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                    <div className="flex items-start gap-2">
                      <AlertTriangle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="font-semibold text-blue-900 mb-1">Plain English</h4>
                        <p className="text-sm text-blue-800">
                          {selectedCookie.category === 'Essential' || selectedCookie.category === 'Necessary' 
                            ? 'This cookie is essential for the website to work properly. It helps with core functionality.' 
                            : selectedCookie.category === 'Analytics' 
                            ? 'This cookie helps understand how visitors use the site by collecting anonymous data.' 
                            : selectedCookie.category === 'Advertising' 
                            ? 'This cookie is used to show you personalized ads based on your browsing behavior.' 
                            : selectedCookie.category === 'Functional' 
                            ? 'This cookie enhances your experience by remembering your preferences.' 
                            : 'This cookie supports website functionality and user experience.'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default CookieScanDashboard;