import {Row, Typography} from "antd";
import {TimeManager} from "../../../../../shared/lib/TimeManager.js";
import {useEffect, useState} from "react";

export function GameHeadbar ({currentMoveTime, score}) {
    const [textGlow, setTextGlow] = useState(20);
    useEffect(() => {
        const interval = setInterval(() => setTextGlow(g => g === 20 ? 30 : 20), 2000);

        return () => clearInterval(interval);
    }, []);
    return (
        <div style={{
            display: 'flex',
            width: '100%',
            height: '7vh',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'linear-gradient(180deg, #0a1428, #001529)',
            marginBottom: 0
        }}>
            <Row>
                <Typography.Title
                    level={3}
                    style={{
                        margin: 0,
                        color: 'white',
                        fontWeight: 500,
                        textShadow: `0 0 ${textGlow}px #ff00cc, 0 0 40px #ff00cc`,
                        letterSpacing: '2px',
                        textTransform: 'uppercase',
                    }}
                >
                    Three&nbsp;
                </Typography.Title>
                <Typography.Title
                    level={3}
                    style={{
                        margin: 0,
                        color: 'white',
                        fontWeight: 500,
                        textShadow: `0 0 ${textGlow}px #a855f7, 0 0 40px #a855f7`,
                        letterSpacing: '2px',
                        textTransform: 'uppercase',
                    }}
                >
                    In&nbsp;
                </Typography.Title>
                <Typography.Title
                    level={3}
                    style={{
                        margin: 0,
                        color: 'white',
                        fontWeight: 500,
                        textShadow: `0 0 ${textGlow}px #22d3ee, 0 0 40px #22d3ee`,
                        letterSpacing: '2px',
                        textTransform: 'uppercase',
                    }}
                >
                    Row
                </Typography.Title>
            </Row>

            <Typography.Title
                level={3}
                style={{
                    margin: 0,
                    color: '#a855f7',
                    fontWeight: 700,
                    textShadow: `0 0 ${textGlow}px #a855f7, 0 0 40px #a855f7`,
                    letterSpacing: '2px',
                    textTransform: 'uppercase',
                }}
            >
                {score}
            </Typography.Title>

            <div style={{
                textAlign: 'right',
                color: '#94a3b8',
                fontSize: '18px',
                fontWeight: 600,
            }}>
                {TimeManager.msToTotalHoursTime(currentMoveTime)} <span
                style={{color: '#64748b'}}>|</span> 2:00:00
            </div>
        </div>
    )
}