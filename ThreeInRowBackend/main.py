from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import config
from src.routers.game import router as game_router
from src.update_looser_games_lifespan import lifespan
from src.routers.create_game import router as create_game_router
from src.routers.difficulties import router as difficulty_router
from src.routers.leaderboard import router as leaderboard_router
from src.exceptions.exceptions_handler import ExceptionCustom, custom_http_exception_handler

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config['front_connection']['hosts'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(create_game_router)
app.include_router(difficulty_router)
app.include_router(game_router)
app.include_router(leaderboard_router)
app.add_exception_handler(ExceptionCustom, custom_http_exception_handler)
