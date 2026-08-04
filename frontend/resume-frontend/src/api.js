import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Standard analysis call
export const analyzeResume = async (file, jdText) => {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("jd_text", jdText);

  const response = await axios.post(`${API_URL}/analyze_resume`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

// Admin History
export const getHistory = async () => {
  const response = await axios.get(`${API_URL}/admin/history`);
  return response.data;
};

// Analytics
export const getAnalytics = async () => {
  const response = await axios.get(`${API_URL}/admin/analytics`);
  return response.data;
};