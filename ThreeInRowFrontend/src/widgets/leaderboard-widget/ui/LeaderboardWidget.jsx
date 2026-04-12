import {useDifficulties} from "../../../entities/difficulty/lib/useDifficulties.js";
import {Col, Radio, Row, Table} from "antd";
import {useNavigate} from "react-router-dom";
import {useBestGamesByDifficulty} from "../../../entities/game/lib/useBestGamesByDifficulty.js";
import "./styles/Table.css";

export function LeaderboardWidget({difficultyId}) {
    const {difficulties, loadingDiff} = useDifficulties();
    const {games, loadingGames} = useBestGamesByDifficulty(difficultyId, 30);
    const navigate = useNavigate();
    const columns = [
        {
            title: 'Уровень сложности',
            dataIndex: 'difficulty_name',
            align: 'center'
        },
        {
            title: 'Итоговое кол-во очков',
            dataIndex: 'score',
            align: 'center'
        },
        {
            title: 'Игровое время',
            dataIndex: 'hours_time',
            align: 'center'
        }
    ];

    function onDifficultyChanged(e) {
        navigate(`/leaderboard/${e.target.value}`);
    }

    return (
        <>
            <Col style={{alignItems: 'center', justifyContent: 'center'}}>
                {!loadingDiff && (
                    <Row justify={'end'} style={{paddingBottom: '1vh'}}>
                        <span>
                            Уровень сложности: <span>
                                <Radio.Group defaultValue={difficultyId} onChange={onDifficultyChanged}> {
                                    difficulties?.map(
                                        (difficulty, index) => (
                                            difficulty.difficulty_name !== "Кастомный" &&
                                            <Radio.Button value={difficulty.id}
                                                          key={index}>{difficulty.difficulty_name}</Radio.Button>
                                        )
                                    )}
                                </Radio.Group>
                            </span>
                        </span>
                    </Row>
                )}
                {!loadingGames && (
                    <Row align={'center'} style={{height: '50vh'}}>
                        <Table theme="dark" dataSource={games} rowKey={"game_id"} columns={columns}
                               pagination={{pageSize: 6, placement: ['bottomCenter']}}/>
                    </Row>
                )}

            </Col>
        </>
    )
}