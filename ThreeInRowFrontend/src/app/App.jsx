import {BrowserRouter, Routes, Route} from 'react-router-dom';
import {CreateGamePage} from '../pages/create-game-page';
import {LeaderboardPage} from "../pages/leaderboard";
import {GamePage} from "../pages/game-page";

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path="/create_game" element={<CreateGamePage/>}/>
                    <Route path="/game/:gameId" element={<GamePage/>}/>
                    <Route path="/leaderboard/:difficultyId" element={<LeaderboardPage/>}/>
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default App
