import {Card, Col, message, Row, Spin} from "antd";
import {GameBoard} from "./game-board";
import {useCurrentGame} from "../../../entities/game/lib/useCurrentGame.js";
import {useEffect, useRef, useState} from "react";
import {patchGameLoose, postRefreshField, postSwap} from "../../../entities/game/api/gamesApi.js";
import {GameState} from "../../../shared/lib/enums.js";
import {CELL_ANIMATION_CONFIG as ANIMATION_CONFIG} from "../../../shared/lib/cssVariablesConfig.js";
import {GameSidebar} from "./sidebar";
import DelimiterLine from "../../../shared/ui/delimiter-line/DelimiterLine.jsx";
import ColorGenerator from "../../../shared/lib/GenerateRandomColor.js";
import {TimeManager} from "../../../shared/lib/TimeManager.js";
import {GameHeadbar} from "./headbar";

export function GameWidget({gameId}) {
    const {game, loading} = useCurrentGame(gameId);
    const [field, setField] = useState(null);
    const [swapLoading, setSwapLoading] = useState(false);
    const [snapshotsArr, setSnapshotsArr] = useState([]);
    const [score, setScore] = useState(0);
    const [destroyedCellsArr, setDestroyedCellsArr] = useState([]);
    const [spawnedCellsArr, setSpawnedCellsArr] = useState([]);
    const [fallenCellsArr, setFallenCellsArr] = useState([]);
    const [isAnimating, setIsAnimating] = useState(false);
    const [gameState, setGameState] = useState(null);
    const [movesInRow, setMovesInRow] = useState(0);
    const [comboDestroys, setComboDestroys] = useState(0);
    const [currentMoveTime, setCurrentMoveTime] = useState(null);
    const colorMapRef = useRef({});

    const getColorForLetter = (letter) => {
        if (!letter) return 'transparent';

        if (!colorMapRef.current[letter]) {
            colorMapRef.current[letter] = ColorGenerator.generateDistinctColor(colorMapRef.current);
        }
        return colorMapRef.current[letter];
    };

    field?.forEach((row, rowIndex) => {
        row.forEach((item, colIndex) => {
            getColorForLetter(item);
            if ((rowIndex === field.length - 1) && (colIndex === field[rowIndex].length - 1) && !(game.random_game_item in colorMapRef.current)) {
                getColorForLetter(game.random_game_item);
            }
        })

    })

    useEffect(() => {
        if (game !== null) {
            setField(game.game_field.field['field']);
            setScore(game.score);
            setGameState(game.is_over && game.lost_of_time ? GameState.LOSE : game.is_over ? GameState.WIN : GameState.PLAYING);
            setCurrentMoveTime(
                game.is_over ? TimeManager.gameLooseTime :
                    game.last_action_time ? Date.now() - new Date(game.last_action_time) : 0
            );
        }
    }, [game]);

    useEffect(() => {
        if (gameState !== null) {
            if (gameState === GameState.PLAYING) {
                const intervalTimer = setInterval(() => {
                    setCurrentMoveTime((prevState) => prevState + 1000);
                }, 1000);
                return () => clearInterval(intervalTimer);
            } else {
                setCurrentMoveTime(TimeManager.gameLooseTime)
            }
        }

    }, [gameState]);

    useEffect(() => {
        if (currentMoveTime >= TimeManager.gameLooseTime && gameState === GameState.PLAYING) {
            setGameState(GameState.LOSE)
            applyGameLoose();
        }
    }, [currentMoveTime]);

    useEffect(() => {
        if (snapshotsArr.length === 0) return;
        setComboDestroys(0);
        setField(snapshotsArr[0].field);
        setScore(snapshotsArr[0].score || 0);
        if (snapshotsArr.length === 1) return;

        let timeouts = [];
        const DESTROY_DURATION = ANIMATION_CONFIG.destroy.ms;
        const FALL_SPAWN_DURATION = ANIMATION_CONFIG.fallSpawn.ms;
        snapshotsArr.forEach((snapshot, index) => {
            const baseDelay = index * (DESTROY_DURATION + FALL_SPAWN_DURATION);

            const destroyId = setTimeout(() => {
                setDestroyedCellsArr(snapshot.items_to_destroy || []);
            }, baseDelay);
            timeouts.push(destroyId);

            const transitionId = setTimeout(() => {
                setDestroyedCellsArr([]);

                if (index < snapshotsArr.length - 1) {
                    setFallenCellsArr(snapshot.items_to_fall || []);
                    const spawnToUse = index < snapshotsArr.length - 1
                        ? (snapshotsArr[index + 1].items_to_spawn || [])
                        : (snapshot.items_to_spawn || []);
                    setSpawnedCellsArr(spawnToUse);
                    setComboDestroys((prevState) => prevState + 1);
                    setField(snapshotsArr[index + 1].field);
                    if (snapshotsArr[index + 1].is_reverted) message.info("Был произведён откат свапа");
                    else if (snapshotsArr[index + 1].is_refreshed) message.info("Поле было полностью обновлено в виду отсутствия потенциальных ходов");
                    setScore(snapshotsArr[index + 1].score || 0);
                    setGameState(snapshotsArr[index + 1].is_over === true ? GameState.WIN : GameState.PLAYING)
                }
            }, baseDelay + DESTROY_DURATION);
            timeouts.push(transitionId);

            const clearId = setTimeout(() => {
                setFallenCellsArr([]);
                setSpawnedCellsArr([]);

                if (index === snapshotsArr.length - 1) {
                    setIsAnimating(false);
                }
            }, baseDelay + DESTROY_DURATION + FALL_SPAWN_DURATION);
            timeouts.push(clearId);
        });

        setIsAnimating(true);

        return () => timeouts.forEach(clearTimeout);
    }, [snapshotsArr]);

    const handleSwap = async (row, col, swap_type) => {
        if (swapLoading || isAnimating) return;
        setSwapLoading(true);
        try {
            const data = await postSwap(gameId, row, col, swap_type);
            setSnapshotsArr(data);
        } catch (error) {
            message.error('Не удалось сделать свап');
        } finally {
            setSwapLoading(false);
            setMovesInRow((prevState) => prevState + 1);
            setCurrentMoveTime(0);
        }
    }
    const handleRefreshFieldButtonClicked = async (scorePenalty = 5) => {
        if (gameState !== GameState.PLAYING) return;
        setSwapLoading(true);
        try {
            const data = await postRefreshField(gameId, scorePenalty);
            setField(data.field);
            setScore(data.score);
            setComboDestroys(0);
            setSpawnedCellsArr(data.items_to_spawn);
            await new Promise(resolve => setTimeout(resolve, ANIMATION_CONFIG.fallSpawn.ms));
        } catch (error) {
            message.error('Не удалось полностью обновить поле');
        } finally {
            setSwapLoading(false);
            setCurrentMoveTime(0);
            setSpawnedCellsArr([]);
        }
    }
    const applyGameLoose = async () => {
        if (gameState !== GameState.PLAYING) return;
        try {
            const data = await patchGameLoose(gameId);
        } catch (error) {
            message.error('Не удалось сдаться');
        } finally {
            setGameState(GameState.LOSE)
        }
    }
    return (
        <>
            {!loading && !game ? (
                <p>Игра не найдена</p>
            ) : !loading && game && field ? (
                    <>
                        {/*<Card style={{background: '#0a1428', border: '1px solid #1f2a44', minWidth: '50%'}}>*/}
                        <Card style={{background: '#001529', border: '1px solid #1f2a44', minWidth: '50%'}}>
                            <Row style={{height: '100%'}}>
                                <Col flex="auto" style={{
                                    marginLeft: 5,
                                    marginRight: 10,
                                    display: 'flex',
                                    flexDirection: 'column',
                                }}>
                                    <Row>
                                        <GameHeadbar currentMoveTime={currentMoveTime} score={score}/>
                                    </Row>
                                    <DelimiterLine type={"horizontal"} boardStyled={true}/>
                                    <Row style={{
                                        flex: 1,
                                        display: 'flex',
                                        justifyContent: 'center',
                                        alignItems: 'center',
                                        padding: '30px 0',
                                        position: 'relative',
                                        minHeight: 0
                                    }}>
                                        <GameBoard
                                            field={field}
                                            onSwap={handleSwap}
                                            destroyedCellsArr={destroyedCellsArr}
                                            spawnedCellsArr={spawnedCellsArr}
                                            fallenCellsArr={fallenCellsArr}
                                            isAnimating={isAnimating}
                                            colorMapRef={colorMapRef.current}
                                            gameState={gameState}
                                            style={{
                                                '--destroy-duration': ANIMATION_CONFIG.destroy.css,
                                                '--fall-spawn-duration': ANIMATION_CONFIG.fallSpawn.css,
                                                position: 'relative'
                                            }}
                                        ></GameBoard>
                                    </Row>
                                </Col>
                                <Col>
                                    <DelimiterLine type={"vertical"} boardStyled={true}/>
                                </Col>
                                <Col>
                                    <GameSidebar
                                        currentItem={game.random_game_item}
                                        currentItemBackgroundColor={colorMapRef.current[game.random_game_item]}
                                        currentScore={score}
                                        targetScore={game.game_rules.target_score}
                                        combo={comboDestroys}
                                        moves={movesInRow}
                                        gameState={gameState}
                                        onRefreshFieldButtonClicked={handleRefreshFieldButtonClicked}
                                        onSurrenderButtonClicked={applyGameLoose}
                                    ></GameSidebar>
                                </Col>
                            </Row>
                        </Card>
                    </>
                ) :
                (
                    <Spin/>
                )
            }
        </>
    );
}