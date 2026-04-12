import {useState, useEffect} from 'react';
import {getDifficulties} from '../api/difficultiesApi.js';
import {message} from 'antd';

export const useDifficulties = () => {
    const [difficulties, setDifficulties] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDifficulties = async () => {
            try {
                const data = await getDifficulties();
                setDifficulties(data);
            } catch (error) {
                message.error('Не удалось загрузить уровни сложности');
                console.error(error);
            } finally {
                setLoading(false);
            }
        };
        fetchDifficulties();
    }, []);

    return {difficulties, loading};
};