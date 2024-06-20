import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // FastAPI server URL
});

// PII Entity APIs
export const getPIIEntities = async (skip = 0, limit = 100) => {
    const response = await api.get('/api/pii_entities', { params: { skip, limit } });
    return response.data;
};

export const createPIIEntity = async (data) => {
    const response = await api.post('/api/pii_entity/', data);
    return response.data;
  };

export const updatePIIEntity = async (entityId, data) => {
    const response = await api.put(`/api/pii_entity/${entityId}`, data);
    return response.data;
};

// Rule APIs
export const getRules = async (skip = 0, limit = 100) => {
    const response = await api.get('/api/rules', { params: { skip, limit } });
    return response.data;
};

export const createRule = async (data) => {
    const response = await api.post('/api/rule/', data);
    return response.data;
};

export const updateRule = async (ruleId, data) => {
    const response = await api.put(`/api/rule/${ruleId}`, data);
    return response.data;
};

// Rule Group Entity Map APIs
export const getRuleGroupEntityMap = async (skip = 0, limit = 100, map = null) => {
    const params = { skip, limit };
    if (map) params.map = map;
    const response = await api.get('/api/rule_group_entity_map', { params });
    return response.data;
};


// PII Identification Record APIs
export const getPIIIdentificationRecords = async (skip = 0, limit = 100, map = null) => {
    const params = { skip, limit };
    if (map) params.map = map;
    const response = await api.get('/api/pii_identification_record', { params });
    return response.data;
};


// Block Rule Score APIs
export const getBlockRuleScores = async (skip = 0, limit = 100, map = null) => {
    const params = { skip, limit };
    if (map) params.map = map;
    const response = await api.get('/api/block_rule_score', { params });
    return response.data;
};
