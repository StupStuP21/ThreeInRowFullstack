import {useEffect, useState} from "react";
import {message} from "antd";
import {getBestGamesByDifficulty} from "../api/gamesApi.js";
import {TimeManager} from "../../../shared/lib/TimeManager.js";

export const useBestGamesByDifficulty = (difficultyId, limitNum) => {
    const [games, setGames] = useState(null);
    const [loading, setLoading] = useState(false);
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getBestGamesByDifficulty(difficultyId, limitNum);
                data.map((game) => {
                    game['hours_time'] = TimeManager.ssToTotalHoursTime(game['game_time_seconds'])
                })
                setGames(data);
            } catch (error) {
                message.error("Не удалось загрузить лучшие игры для данной сложности")
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [difficultyId]);
    return {games, loading};
}