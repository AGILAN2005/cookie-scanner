import React, { useState, useEffect } from 'react';
import { X, Plus } from 'lucide-react';
import Sidebar from '../components/Sidebar';
import HeaderTabs from '../components/HeaderTabs';
import StatsCard from '../components/StatsCard';
import SearchBar from '../components/SearchBar';
import SitesTable from '../components/SitesTable';
import AddSiteModal from '../components/AddSiteModal';
import Dashboard from './Dashboard';

import { getSites, addSite, updateSite, deleteSite,getScanResult, getJobStatus } from '../services/api';

const SitesManagement = () => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('All');
  const [selectedSite, setSelectedSite] = useState(null);
  const [showDashboard, setShowDashboard] = useState(false);
  const [sites, setSites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [scanData, setScanData] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [editingSite, setEditingSite] = useState(null); 
  const [formData, setFormData] = useState({ siteUrl: '', version: '', ownerName: '', ownerEmail: '', type: 'ROOT' });

  useEffect(() => {
    fetchSites();
  }, []);

  const fetchSites = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getSites();
      setSites(response.data || []);
    } catch (error) {
      setError(error.message);
      console.error('Error fetching sites:', error);
    } finally {
      setLoading(false);
    }
  };

   const handleOpenAddModal = () => {
    setEditingSite(null);
    setFormData({ siteUrl: '', version: '', ownerName: '', ownerEmail: '', type: 'ROOT' });
    setShowAddModal(true);
  };

  const handleOpenEditModal = (site) => {
    setEditingSite(site);
    setFormData({
      siteUrl: site.url,
      version: site.version,
      ownerName: site.owner,
      ownerEmail: site.ownerEmail || '', 
      type: site.type
    });
    setShowAddModal(true);
  };

  const handleAddOrUpdateSite = async () => {
    if (!formData.siteUrl || !formData.version || !formData.ownerName) {
      setError('Please fill in all required fields.');
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      if (editingSite) {
      
        await updateSite(editingSite.id, {
          version: formData.version,
          owner_name: formData.ownerName,
          owner_email: formData.ownerEmail,
          type: formData.type,
        });
        alert('✓ Site updated successfully!');
      } else {
       
        await addSite({ url: formData.siteUrl, ...formData });
        alert('✓ Site added successfully and scan initiated!');
      }
      setShowAddModal(false);
      fetchSites();
    } catch (error) {
      setError(error.message);
      console.error('Error submitting site:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteSite = async (site) => {
    if (window.confirm(`Are you sure you want to delete ${site.url}? This will delete all associated scan history.`)) {
      try {
        await deleteSite(site.id);
        alert('✓ Site deleted successfully.');
        setSites(sites.filter(s => s.id !== site.id));
      } catch (error) {
        alert(`❌ Error deleting site: ${error.message}`);
        console.error('Error deleting site:', error);
      }
    }
  };
  
  const handleRescan = async (siteToRescan) => {
    if (window.confirm(`Are you sure you want to re-scan ${siteToRescan.url}?`)) {
      try {
       
        const fullSiteDetails = sites.find(s => s.id === siteToRescan.id);
        if (!fullSiteDetails) {
            alert('Could not find site details to initiate re-scan.');
            return;
        }
        await addSite({
          url: fullSiteDetails.url,
          type: fullSiteDetails.type,
          version: fullSiteDetails.version,
          ownerName: fullSiteDetails.owner,
          ownerEmail: fullSiteDetails.ownerEmail || '',
        });
        alert('✓ Re-scan initiated successfully!');
        handleBackToSites();
      } catch (error) {
        alert(`❌ Error initiating re-scan: ${error.message}`);
      }
    }
  };

  const handleViewDetails = async (site) => {
    try {
      setLoading(true);
      setError(null);
      setSelectedSite(site);
      
      if (!site.lastScanJobId) {
        alert('⏳ This site has not been scanned yet.');
        setLoading(false);
        return;
      }

      const statusResponse = await getJobStatus(site.lastScanJobId);
      const { status, error: errorMsg } = statusResponse.data;
      
      if (status === 'COMPLETED') {
        const scanResponse = await getScanResult(site.lastScanJobId);
        setScanData(scanResponse.data);
        setShowDashboard(true);
      } else if (status === 'FAILED') {
        alert(`❌ Scan failed\n\nError: ${errorMsg || 'Unknown error'}`);
      } else if (['RUNNING', 'ENRICHING', 'QUEUED'].includes(status)) {
        alert(`⏳ Scan is currently ${status}. Please wait a moment and try again.`);
      } else {
        alert(`ℹ️ Unknown scan status: ${status}.`);
      }
    } catch (error) {
      setError(error.message);
      console.error('Error loading scan data:', error);
      alert(`❌ Error loading scan data: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToSites = () => {
    setShowDashboard(false);
    setSelectedSite(null);
    setScanData(null);
    fetchSites();
  };

  const filteredSites = sites.filter(site => {
    const searchLower = searchTerm.toLowerCase();
    const matchesSearch = 
      (site.url && site.url.toLowerCase().includes(searchLower)) ||
      (site.siteId && site.siteId.toLowerCase().includes(searchLower)) ||
      (site.owner && site.owner.toLowerCase().includes(searchLower));
    const matchesFilter = filterStatus === 'All' || site.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const stats = {
    total: sites.length,
    published: sites.filter(s => s.status === 'PUBLISHED').length,
    pending: sites.filter(s => s.status === 'PENDING').length
  };

  if (showDashboard && selectedSite && scanData) {
    return (
        <div className="min-h-screen bg-gray-50">
            <Sidebar />
            <div className="ml-48">
                <div className="p-6 bg-white border-b border-gray-200">
                    <button onClick={handleBackToSites} className="flex items-center gap-2 text-indigo-600 hover:text-indigo-800 font-medium">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
                        Back to Sites
                    </button>
                </div>
                 <Dashboard scanResult={scanData} onRescan={() => handleRescan(selectedSite)} />
            </div>
        </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="ml-48 p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-normal text-gray-400 mb-6">Sites Management</h1>
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 flex items-start gap-2">
              <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" /></svg>
              <div>
                <div className="font-semibold">Error</div>
                <div className="text-sm">{error}</div>
              </div>
              <button onClick={() => setError(null)} className="ml-auto text-red-500 hover:text-red-700">
                <X className="w-5 h-5" />
              </button>
            </div>
          )}
          <HeaderTabs />
          <StatsCard stats={stats} />
          <SearchBar 
            searchTerm={searchTerm} setSearchTerm={setSearchTerm}
            filterStatus={filterStatus} setFilterStatus={setFilterStatus}
            onAddClick={handleOpenAddModal}
          />
          {loading ? (
            <div className="text-center py-12"><div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div><p className="mt-4 text-gray-600">Loading sites...</p></div>
          ) : sites.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-12 text-center"><svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg><h3 className="mt-2 text-sm font-medium text-gray-900">No sites found</h3><p className="mt-1 text-sm text-gray-500">Get started by adding a new site.</p><div className="mt-6"><button onClick={() => setShowAddModal(true)} className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"><Plus className="w-4 h-4 mr-2" />Add Site</button></div></div>
          ) : (
            <SitesTable sites={filteredSites} onViewDetails={handleViewDetails} onEdit={handleOpenEditModal} onDelete={handleDeleteSite}
              />
          )}
        </div>
      </div>
      <AddSiteModal 
        showModal={showAddModal}
        onClose={() => { setShowAddModal(false); setError(null); }}
        formData={formData}
        setFormData={setFormData}
        onSubmit={handleAddOrUpdateSite}
        loading={submitting}
        error={error}
        isEditing={!!editingSite}
      />
    </div>
  );
};

export default SitesManagement;