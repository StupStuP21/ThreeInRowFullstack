import './styles/Arrow.css';
import {SwapDirections} from "../../lib/enums.js";

export default function Arrow({arrowDirection, positioned, ...rest}) {
    return (
        <div
            className={`arrow ${positioned ? `positioned ${arrowDirection}` : ''}`}
            {...rest}
        >
            {
                arrowDirection === SwapDirections.UP ? '\u21E7' :
                    arrowDirection === SwapDirections.DOWN ? '\u21E9' :
                        arrowDirection === SwapDirections.LEFT ? '\u21E6' : '\u21E8'
            }

        </div>
    )
}