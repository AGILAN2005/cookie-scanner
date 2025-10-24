import React from 'react';

const HeaderTabs = () => {
  return (
    <div className="flex gap-6 border-b border-gray-200 mb-6">
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        Systems
      </button>
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        System Policy
      </button>
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        System Purpose
      </button>
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        Vendor
      </button>
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        Data Category
      </button>
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        Data
      </button>
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        Purpose Category
      </button>
      <button className="pb-3 text-gray-500 hover:text-gray-700">
        Frequency
      </button>
      <button className="pb-3 text-purple-600 border-b-2 border-purple-600 font-medium">
        Sites/Domains
      </button>
    </div>
  );
};

export default HeaderTabs;