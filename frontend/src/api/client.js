import axios from 'axios';

const api = axios.create({
    baseURL: '/api',
    timeout: 120000, // 2 min — model loading can be slow first time
    headers: { 'Accept': 'application/json' },
});

// ── Health ──────────────────────────────────────────────────────────
export const checkHealth = () => api.get('/health');

// ── Resume Upload ──────────────────────────────────────────────────
export const uploadResume = (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
};

// ── Analysis ───────────────────────────────────────────────────────
export const analyzeMatch = (resumeText, jobDescription) =>
    api.post('/analysis/match', {
        resume_text: resumeText,
        job_description: jobDescription,
    });

export default api;
