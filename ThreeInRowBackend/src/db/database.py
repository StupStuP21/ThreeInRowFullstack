from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.project_settings_parser import SettingsParser

parser = SettingsParser()
parser.create_settings_file()
config = parser.get_settings()

DATABASE_URL = f"postgresql+asyncpg://{config['db_connection']['db_user']}:{config['db_connection']['db_password']}@{config['db_connection']['db_host']}:{config['db_connection']['db_port']}/{config['db_connection']['db_name']}"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
