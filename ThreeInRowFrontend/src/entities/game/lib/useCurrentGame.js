import {useEffect, useState} from "react";
import {getCurrentGame} from "../api/gamesApi.js";
import {message} from "antd";

export const useCurrentGame = (id) => {
    const [game, setGame] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getCurrentGame(id);
                setGame(data);
            } catch (err) {
                message.error('Не удалось загрузить текущую игру');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id]);
    return {game, loading};
};