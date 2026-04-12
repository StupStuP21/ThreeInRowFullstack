import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const getDifficulties = async () => {
    const response = await axios.get(`${API_URL}/difficulties`);
    return response.data.sort((a, b) => { if (a.id < b.id) { return -1; } });
};

export const getDifficultyById = async(id) => {
    const response = await axios.get(`${API_URL}/difficulties/${id}`);
    return response.data
}

export const getCustomDifficulty = async () => {
    const response = await axios.get(`${API_URL}/difficulties`, {params: {name: "Кастомный"}})
    return response.data[0]
}