import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

// Standard analysis call
export const analyzeResume = async (file, jdText) => {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("jd_text", jdText);

  const response = await axios.post(`${API_URL}/analyze_resume`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
};

// --- NEW EXPORTS: ADD THESE BELOW ---

export const getHistory = async () => {
  const response = await axios.get(`${API_URL}/admin/history`);
  return response.data;
};

export const getAnalytics = async () => {
  const response = await axios.get(`${API_URL}/admin/analytics`);
  return response.data;
};