import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // Или вынеси в .env как import.meta.env.VITE_API_URL

export const getCurrentGame = async (id) => {
    const response = await axios.get(`${API_URL}/game/${id}`);
    return response.data;
}

export const postGame = async (values) => {
    const response = await axios.post(`${API_URL}/create_game/create`, {
        row_count: values.num_row,
        col_count: values.num_col,
        target_score: values.target_score,
        game_items_count: values.num_game_items,
        is_one_swap_mode: values.one_swap_mode,
        is_one_item_mode: values.random_item_mode,
        game_difficulty_id: values.game_difficulty
    })
    return (response !== undefined) ? response.data : {};
};

export const postSwap = async (gameId, row_num, col_num, swap_type) => {
    const response = await axios.post(`${API_URL}/game/${gameId}/swap`, {}, {
        params: {
            row_num: row_num,
            col_num: col_num,
            swap_type: swap_type
        }
    })
    return (response !== undefined) ? response.data : {};
}

export const postRefreshField = async (gameId, scorePenalty) => {
    const response = await axios.post(`${API_URL}/game/${gameId}/refresh`, {}, {
        params: {
            score_penalty: scorePenalty
        }
    })
    return (response !== undefined) ? response.data : {}
}

export const patchGameLoose = async (gameId) => {
    const response = await axios.patch(`${API_URL}/game/${gameId}`, {
        is_over: true,
        lost_of_time: true
    })
    return (response !== undefined) ? response.data : {};
}

export const getBestGamesByDifficulty = async (difficultyId, limitNumber=10) => {
    const response = await axios.get(`${API_URL}/leaderboard/${difficultyId}`, {}, {
            params: {
                limit: limitNumber
            }
        });
    return (response !== undefined) ? response.data : [];
}