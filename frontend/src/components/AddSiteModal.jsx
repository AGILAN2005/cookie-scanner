import React from 'react';
import { X } from 'lucide-react';

const AddSiteModal = ({ showModal, onClose, formData, setFormData, onSubmit, loading, error, isEditing }) => {
  if (!showModal) return null;

  return (
    <div 
      className="fixed inset-0 bg bg-opacity-5 backdrop-blur flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      
      <div 
        className="bg-white rounded-lg w-full max-w-2xl shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">{isEditing ? 'Edit Site' : 'Add Site'}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            disabled={loading}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Site URL <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                placeholder="https://example.com"
                value={formData.siteUrl}
                onChange={(e) => setFormData({...formData, siteUrl: e.target.value})}
               disabled={loading || isEditing}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white text-gray-900 disabled:bg-gray-100 disabled:cursor-not-allowed"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Version <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                placeholder="1.0"
                value={formData.version}
                onChange={(e) => setFormData({...formData, version: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white text-gray-900"
                disabled={loading}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Owner Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                placeholder="John Doe"
                value={formData.ownerName}
                onChange={(e) => setFormData({...formData, ownerName: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white text-gray-900"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Owner Email ID
              </label>
              <input
                type="email"
                placeholder="john@example.com"
                value={formData.ownerEmail}
                onChange={(e) => setFormData({...formData, ownerEmail: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white text-gray-900"
                disabled={loading}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Domain Type
            </label>
            <div className="flex gap-6">
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="type"
                  value="ROOT"
                  checked={formData.type === 'ROOT'}
                  onChange={(e) => setFormData({...formData, type: e.target.value})}
                  className="w-4 h-4 text-purple-600 focus:ring-purple-500"
                  disabled={loading}
                />
                <span className="ml-2 text-sm text-gray-700">Root Domain</span>
              </label>
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="type"
                  value="SUB DOMAIN"
                  checked={formData.type === 'SUB DOMAIN'}
                  onChange={(e) => setFormData({...formData, type: e.target.value})}
                  className="w-4 h-4 text-purple-600 focus:ring-purple-500"
                  disabled={loading}
                />
                <span className="ml-2 text-sm text-gray-700">Sub Domain</span>
              </label>
            </div>
          </div>
        </div>

        <div className="p-6">
          <button
            onClick={onSubmit}
            disabled={loading}
            className="w-full py-3 bg-pink-500 hover:bg-pink-600 text-white font-medium rounded-lg transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>{isEditing ? 'Updating...' : 'Submitting...'}</span>
              </>
            ) : (
              isEditing ? 'Update Site' : 'Add Site & Scan'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddSiteModal;