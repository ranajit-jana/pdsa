import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // FastAPI server URL
});

export const getBlockRuleScores = async () => {
    const response = await api.get('/api/block_rule_score');
    return response.data;
};

export const createBlockRuleScore = async (data) => {
    const response = await api.post('/api/block_rule_score', data);
    return response.data;
};

// Add other API methods as needed
