from fastapi import Depends

from app.db.uow import UnitOfWork, get_uow
from app.logic.user.service import UserService

def get_user_service(uow: UnitOfWork = Depends(get_uow), service: UserService = Depends(get_uow)) -> UserService:
    return UserService(lambda: uow)