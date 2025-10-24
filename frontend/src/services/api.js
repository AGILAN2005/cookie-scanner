import axios from 'axios';

const API_URL = 'http://localhost:8001';

axios.interceptors.response.use(
  response => response,
  error => {
    const message = error.response?.data?.detail || error.message || 'An error occurred';
    return Promise.reject(new Error(message));
  }
);

export const getSites = () => {
  return axios.get(`${API_URL}/sites`);
};

export const addSite = (siteData) => {
  return axios.post(`${API_URL}/scan`, {
    url: siteData.url,
    type: siteData.type,
    version: siteData.version,
    ownerName: siteData.ownerName, 
    ownerEmail: siteData.ownerEmail,
    options: {
      accept_consent: true,
      simulate_user_actions: ["scroll"],
      headless: true,
      wait_seconds: 10
    }
  });
};

export const updateSite = (siteId, siteData) => {
  return axios.put(`${API_URL}/site/${siteId}`, siteData);
};

export const deleteSite = (siteId) => {
  return axios.delete(`${API_URL}/site/${siteId}`);
};

export const getScanResult = (jobId) => {
  return axios.get(`${API_URL}/result/${jobId}`);
};

export const getJobStatus = (jobId) => {
  return axios.get(`${API_URL}/status/${jobId}`);
};

export const getSiteLatestScan = (siteId) => {
  return axios.get(`${API_URL}/site/${siteId}/latest-scan`);
};