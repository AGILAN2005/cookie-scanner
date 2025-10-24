import React from 'react';

const Sidebar = () => {
  return (
    <div className="fixed left-0 top-0 h-full w-48 bg-white border-r border-gray-200 overflow-y-auto">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-700">ATLAS</h2>
      </div>
      
      <nav className="p-2">
        <div className="mb-4">
          <div className="px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">
            Dashboard
          </div>
        </div>

        <div className="mb-4">
          <div className="px-3 py-2 text-sm font-semibold text-gray-700">KYC Manager</div>
          <div className="ml-2">
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Checks</div>
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Designer</div>
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Verification</div>
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Signature</div>
          </div>
        </div>

        <div className="mb-4">
          <div className="px-3 py-2 text-sm font-semibold text-gray-700">Privacy Manager</div>
          <div className="ml-2">
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Dashboard</div>
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Assessment</div>
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Discovery</div>
            <div className="px-3 py-1 text-sm bg-purple-50 text-purple-700 rounded cursor-pointer font-medium">Sites</div>
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Consents</div>
            <div className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">Notices</div>
          </div>
        </div>

        <div className="px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">
          Admin
        </div>
        
        <div className="px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded cursor-pointer">
          Log Out
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;