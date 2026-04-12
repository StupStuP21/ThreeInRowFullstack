import './styles/GameFieldCell.css';
import Arrow from "../../../../../../../shared/ui/arrow/Arrow.jsx";
import {SwapDirections} from "../../../../../../../shared/lib/enums.js";
import {CELL_VARS_CONFIG} from "../../../../../../../shared/lib/cssVariablesConfig.js";

export function GameFieldCell({
                                  children,
                                  rowIndex,
                                  colIndex,
                                  cellColor,
                                  rowArrLength,
                                  rowNumber,
                                  isSelected,
                                  handleCellClick,
                                  handleCellArrowClick,
                                  isDestroyed,
                                  isSpawned,
                                  isFallen,
                                  fallDistance,
                                  fontSize,
                                  ...rest
                              }) {
    return (
        <div
            {...rest}
        >
            <div
                className={
                    `cell 
                        ${isSelected ? 'selected' : ''} 
                        ${isDestroyed ? 'destroying' : ''}
                        ${isSpawned ? 'spawning' : ''}
                        ${isFallen ? 'falling' : ''}
                    `
                }
                style={{
                    backgroundColor: cellColor,
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    cursor: "pointer",
                    ...(isFallen && {
                        '--fall-distance': `-${fallDistance * (CELL_VARS_CONFIG.height.px + CELL_VARS_CONFIG.margin.px)}px`,
                    }),
                    ...(isSpawned && {
                        '--spawn-distance': `-${(rowIndex + 2) * (CELL_VARS_CONFIG.height.px + CELL_VARS_CONFIG.margin.px)}px`,
                    }),
                    ...(fontSize && {
                        // 'font-size': `${fontSize}px`
                        'fontSize': `${fontSize}px`
                    })
                }}
            >
                {children}
            </div>

            {isSelected && (
                <>
                    {
                        rowIndex !== 0 && (
                            <Arrow arrowDirection={SwapDirections.UP} positioned={true}
                                   onClick={() => handleCellArrowClick(rowIndex, colIndex, SwapDirections.UP)}/>
                        )
                    }
                    {
                        rowIndex + 1 !== rowNumber && (
                            <Arrow arrowDirection={SwapDirections.DOWN} positioned={true}
                                   onClick={() => handleCellArrowClick(rowIndex, colIndex, SwapDirections.DOWN)}/>
                        )
                    }
                    {
                        colIndex !== 0 && (
                            <Arrow arrowDirection={SwapDirections.LEFT} positioned={true}
                                   onClick={() => handleCellArrowClick(rowIndex, colIndex, SwapDirections.LEFT)}/>
                        )
                    }
                    {
                        colIndex + 1 !== rowArrLength && (
                            <Arrow arrowDirection={SwapDirections.RIGHT} positioned={true}
                                   onClick={() => handleCellArrowClick(rowIndex, colIndex, SwapDirections.RIGHT)}/>
                        )
                    }
                </>
            )}
        </div>
    )
}