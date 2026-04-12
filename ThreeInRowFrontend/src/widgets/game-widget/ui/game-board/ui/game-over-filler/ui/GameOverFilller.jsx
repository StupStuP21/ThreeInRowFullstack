import DelimiterLine from "../../../../../../../shared/ui/delimiter-line/DelimiterLine.jsx";
import {GameState} from "../../../../../../../shared/lib/enums.js";
import {Typography} from "antd";

export function GameOverFiller({field, gameState}) {
    return (
        <>
            <div style={{
                position: 'absolute',
                inset: 0,
                background: 'rgba(0, 0, 0, 0.6)',
                backdropFilter: 'blur(1px)',
                zIndex: 10
            }}/>

            <div style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 20,
                textAlign: 'center'
            }}>
                <DelimiterLine type={'horizontal'} boardStyled={false}
                               style={{background: 'black', height: '5px'}}></DelimiterLine>
                <Typography.Title
                    level={1}
                    style={{
                        margin: 0,
                        color: '#ff4d4f',
                        justifyContent: 'center',
                        fontSize: field[0].length > 6 ? '3rem' : '100%',
                        fontWeight: 900,
                        textShadow: '0 0 30px #ff0000, 0 0 60px #ff4d4f',
                        textTransform: 'uppercase',
                        letterSpacing: '4px',
                    }}
                >
                    {gameState === GameState.LOSE ? 'ПОРАЖЕНИЕ' : 'ПОБЕДА'}
                </Typography.Title>
                <DelimiterLine type={'horizontal'} boardStyled={false}
                               style={{background: 'black', height: '5px'}}></DelimiterLine>
            </div>
        </>
    )
}