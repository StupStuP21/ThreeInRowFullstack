from fastapi import FastAPI

from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.services.games_service import GameService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Здесь создаётся шедулер для проверки игр на бездействие и обновление их состояния игрового состояния,
    если 2 часа в бездействии
    :param app:
    :return:
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        GameService.update_losing_games,
        trigger=IntervalTrigger(minutes=1)
    )
    scheduler.start()
    print("Scheduler started")

    yield

    scheduler.shutdown()
    print("Scheduler shutdown")
