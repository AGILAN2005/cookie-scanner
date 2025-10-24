import React from 'react';

const StatsCard = ({ stats }) => {
  return (
    <div className="flex gap-8 mb-6">
      <div>
        <div className="text-2xl font-semibold text-purple-600">{stats.total}</div>
        <div className="text-sm text-gray-600">Total</div>
      </div>
      <div>
        <div className="text-2xl font-semibold text-purple-600">{stats.published}</div>
        <div className="text-sm text-gray-600">Published</div>
      </div>
      <div>
        <div className="text-2xl font-semibold text-purple-600">{stats.pending}</div>
        <div className="text-sm text-gray-600">Pending</div>
      </div>
    </div>
  );
};

export default StatsCard;