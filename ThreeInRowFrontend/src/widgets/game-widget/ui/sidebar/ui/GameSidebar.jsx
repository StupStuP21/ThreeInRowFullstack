import {Button, Progress, Typography} from 'antd';
import {ReloadOutlined, FlagOutlined} from '@ant-design/icons';
import DelimiterLine from "../../../../../shared/ui/delimiter-line/DelimiterLine.jsx";
import {GameFieldCell} from "../../game-board";
import {GameState} from "../../../../../shared/lib/enums.js";

export function GameSidebar(
    {
        currentItem,
        currentItemBackgroundColor,
        currentScore,
        targetScore,
        combo,
        moves,
        gameState,
        onRefreshFieldButtonClicked,
        onSurrenderButtonClicked
    }
) {
    return (
        <div style={
            {
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                height: '100%'
            }
        }>
            <div style={{
                width: '100%'
            }}>
                <div style={{height: '7vh'}}>
                    <Button
                        type="primary"
                        icon={<ReloadOutlined/>}
                        disabled={gameState !== GameState.PLAYING}
                        size="large"
                        block
                        onClick={() => onRefreshFieldButtonClicked()}
                        style={{
                            background: 'linear-gradient(90deg, #00d4ff, #a855f7)',
                            border: 'none',
                            color: '#fff',
                            fontWeight: 600,
                            boxShadow: '0 0 20px rgba(168, 85, 247, 0.65)',
                            transition: 'all 0.3s ease',
                            height: 56,
                        }}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.background = 'linear-gradient(90deg, #67e8f9, #c026d3)';
                            e.currentTarget.style.boxShadow = '0 0 25px rgba(192, 38, 211, 0.8)';
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.background = 'linear-gradient(90deg, #00d4ff, #a855f7)';
                            e.currentTarget.style.boxShadow = '0 0 20px rgba(168, 85, 247, 0.65)';
                        }}
                    >
                        Обновить поле
                    </Button>
                    <DelimiterLine type={"horizontal"} boardStyled={true} style={{marginTop: '0.5vh'}}/>
                </div>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    height: '30vh'
                }}>
                    <Typography.Title level={4} style={{color: '#fff', textAlign: 'center'}}>Текущий игровой
                        предмет</Typography.Title>
                    <GameFieldCell
                        cellColor={currentItemBackgroundColor}
                        isSelected={false}
                        isDestroyed={false}
                        isSpawned={false}
                        isFallen={false}
                        handleCellClick={() => {
                        }}
                        handleCellArrowClick={() => {
                        }}
                        fontSize={90}
                        style={{
                            width: '75%',
                            height: '75%'
                        }}
                    >{currentItem}</GameFieldCell>
                    <Typography.Text type="secondary" style={{color: '#fff'}}>Даёт +1 очко</Typography.Text>
                </div>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}>
                    <Typography.Title level={4} style={{color: '#fff', textAlign: 'center'}}>Текущая
                        цель</Typography.Title>


                    <Progress
                        percent={currentScore ? Math.round(currentScore / targetScore * 100) : 0}
                        strokeColor="#00ff88"
                        railColor={"#1f2a44"}
                        size={['100%', 30]}
                        strokeLinecap="round"
                        style={{
                            borderRadius: 0,
                            padding: '4px 0',
                            width: '100%'
                        }}
                        percentPosition={{type: 'inner', align: 'center'}}
                    />
                    <Typography.Text type="secondary"
                                     style={{color: '#fff'}}>{currentScore}/{targetScore}</Typography.Text>
                </div>

                <div>
                    <Typography.Title level={3} style={{color: '#fff', textAlign: 'center'}}>
                        Ходы: {moves}
                    </Typography.Title>

                    <Typography.Text strong style={{color: '#ffd700'}}>Комбо: x{combo}</Typography.Text>
                </div>
            </div>
            <div>
                <Button
                    type="primary"
                    danger icon={<FlagOutlined/>}
                    onClick={() => onSurrenderButtonClicked()}
                    block
                    size="large"
                    style={{marginTop: 10}}
                >
                    Сдаться
                </Button>
            </div>
        </div>
    )
};