import './styles/GameBoard.css';
import {useState} from "react";
import {GameFieldCell} from "./game-board-cell";
import {CELL_VARS_CONFIG} from "../../../../../shared/lib/cssVariablesConfig.js";
import {GameState} from "../../../../../shared/lib/enums.js";
import {GameOverFiller} from "./game-over-filler";

export function GameBoard(
    {
        field,
        onSwap,
        destroyedCellsArr,
        fallenCellsArr,
        spawnedCellsArr,
        isAnimating,
        colorMapRef,
        gameState,
        style
    }
) {
    const [selectedCell, setSelectedCell] = useState(null);

    const handleCellClick = (rowIndex, colIndex) => {
        if (isAnimating) return;
        if (!selectedCell) {
            setSelectedCell({row: rowIndex, col: colIndex});
            return;
        }
        setSelectedCell(null);
    };
    const handleCellArrowClick = (rowIndex, colIndex, swapDirection) => {
        onSwap(rowIndex, colIndex, swapDirection)
    }

    return (
        <div className="board"
             style={
                 {
                     display: "inline-block",
                     overflow: 'visible',
                     ...style
                 }
             }>
            {field.map((row, rowIndex) => (
                <div key={rowIndex} className="row"
                     style={{display: "flex"}}>
                    {row.map((cell, colIndex) => {
                        const color = colorMapRef[cell];
                        const isSelected = selectedCell?.row === rowIndex && selectedCell?.col === colIndex;
                        const isDestroyed = destroyedCellsArr.some(coord =>
                            coord[0] === rowIndex && coord[1] === colIndex);
                        const isSpawned = spawnedCellsArr.some(coord =>
                            coord[0] === rowIndex && coord[1] === colIndex);
                        const isFallen = fallenCellsArr.some(coord =>
                            coord[0] === rowIndex && coord[1] === colIndex);
                        const fallDistance = fallenCellsArr.find(coord =>
                            coord[0] === rowIndex && coord[1] === colIndex)?.[2] || 0
                        return (
                            <GameFieldCell
                                rowIndex={rowIndex}
                                colIndex={colIndex}
                                cellColor={color}
                                rowArrLength={row.length}
                                rowNumber={field.length}
                                isSelected={isSelected}
                                isDestroyed={isDestroyed}
                                isSpawned={isSpawned}
                                isFallen={isFallen}
                                fallDistance={fallDistance}
                                handleCellClick={handleCellClick}
                                handleCellArrowClick={handleCellArrowClick}
                                key={`${rowIndex}-${colIndex}`}
                                style={{
                                    position: "relative",
                                    width: CELL_VARS_CONFIG.width.css,
                                    height: CELL_VARS_CONFIG.height.css,
                                    margin: CELL_VARS_CONFIG.margin.css,
                                    fontSize: CELL_VARS_CONFIG.fontSize.css,
                                    borderRadius: CELL_VARS_CONFIG.borderRadius.css,
                                }}
                                onClick={() => handleCellClick(rowIndex, colIndex)}
                            >
                                {cell}
                            </GameFieldCell>
                        );
                    })}
                </div>
            ))}
            {gameState !== GameState.PLAYING && (
                <GameOverFiller field={field} gameState={gameState}></GameOverFiller>
            )}
        </div>
    );
}