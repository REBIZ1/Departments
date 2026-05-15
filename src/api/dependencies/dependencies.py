from typing import Annotated
from fastapi import Depends

from src.database import async_session_maker
from src.utils.db_manager import DBManager


async def get_db():
    """
    Создает асинхронную сессию базы данных через DBManager
    и автоматически закрывает её после завершения запроса

    yield:
        DBManager: Экземпляр менеджера базы данных
    """
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
