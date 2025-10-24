import React, { useState, useRef } from 'react';
import ReactDOM from 'react-dom';
import { MoreVertical, Eye, Edit, Trash2 } from 'lucide-react';


const DropdownMenu = ({ targetRect, onClose, children }) => {
  
  const isUp = (window.innerHeight - targetRect.bottom) < 150; 

  const style = {
    top: isUp ? 'auto' : `${targetRect.bottom + window.scrollY + 5}px`, 
    bottom: isUp ? `${window.innerHeight - targetRect.top - window.scrollY + 5}px` : 'auto',
    left: `${targetRect.left - 160}px`, 
  };

  return ReactDOM.createPortal(
    <>
      <div className="fixed inset-0 z-40" onClick={onClose} />
      <div style={style} className="absolute w-48 bg-white rounded-lg shadow-lg border py-1 z-50 animate-fade-in-fast">
        {children}
      </div>
    </>,
    document.body
  );
};


const SiteTableRow = ({ site, index, onViewDetails, onEdit }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const buttonRef = useRef(null);

  // const handleDropdownToggle = () => {
  //   if (!showDropdown) {
  //     const rect = buttonRef.current.getBoundingClientRect();
  //     const spaceBelow = window.innerHeight - rect.bottom;
 
  //   }
  //   setShowDropdown(!showDropdown);
  // };

  const getScanStatusColor = (status) => {
    const colors = { 'COMPLETED': 'bg-green-100 text-green-700', 'RUNNING': 'bg-blue-100 text-blue-700', 'FAILED': 'bg-red-100 text-red-700', 'PENDING': 'bg-yellow-100 text-yellow-700', 'QUEUED': 'bg-gray-100 text-gray-700', 'ENRICHING': 'bg-purple-100 text-purple-700' };
    return colors[status] || 'bg-gray-100 text-gray-700';
  };
  const getStatusColor = (status) => status === 'PUBLISHED' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700';

  return (
    <tr className="hover:bg-gray-50">
      <td className="px-4 py-3 text-sm text-gray-700">{index + 1}</td>
      <td className="px-4 py-3 text-sm text-gray-700 font-mono">{site.siteId}</td>
      <td className="px-4 py-3 text-sm text-blue-600 hover:underline cursor-pointer truncate" style={{ maxWidth: '200px' }}>{site.url}</td>
      <td className="px-4 py-3"><span className={`px-2 py-1 rounded-full text-xs font-medium ${getScanStatusColor(site.scanStatus)}`}>{site.scanStatus}</span></td>
      <td className="px-4 py-3 text-sm text-gray-700">{site.type}</td>
      <td className="px-4 py-3 text-sm text-gray-700">{site.version}</td>
      <td className="px-4 py-3 text-sm text-gray-700">{site.owner}</td>
      <td className="px-4 py-3 text-sm text-gray-600">{site.created}</td>
      <td className="px-4 py-3 text-sm text-gray-600">{site.updated}</td>
      <td className="px-4 py-3"><span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(site.status)}`}>{site.status}</span></td>
      <td className="px-4 py-3">
        <button 
          ref={buttonRef} 
          onClick={() => setShowDropdown(true)}
          className="p-1 hover:bg-gray-200 rounded-full"
        >
          <MoreVertical className="w-4 h-4 text-gray-600" />
        </button>

        {showDropdown && (
  <DropdownMenu 
    targetRect={buttonRef.current.getBoundingClientRect()}
    onClose={() => setShowDropdown(false)}
  >
    <button
      onClick={() => { onViewDetails(site); setShowDropdown(false); }}
      className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
    >
      <Eye className="w-4 h-4" /> Show Details
    </button>
    <button
              onClick={() => { onEdit(site); setShowDropdown(false); }}
              className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
            >
              <Edit className="w-4 h-4" /> Edit Site
            </button>
            {/* <button
              onClick={() => { onDelete(site); setShowDropdown(false); }}
              className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" /> Delete Site
            </button> */}
  </DropdownMenu>
)}
      </td>
    </tr>
  );
};

export default SiteTableRow;