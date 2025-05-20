from fastapi import APIRouter,Depends,Path
from ..schemas import users
from ..repository import user_queries
from typing import Any
from . import middleware
from ..service.jwt_hand import Payloads
router=APIRouter(
    prefix="/api/users",tags=["users"]

)


@router.get("/user",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def print_user_by_id(user:Payloads=Depends(middleware.checkautherization))->Any:
    return await user_queries.get_user_by_id(user.user_id)

@router.put("/user",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def edit_user(uuser:users.User=Depends(),user:Payloads=Depends(middleware.checkautherization))->Any:
    if user.user_id==1:
        uuser.role="admin"
        return await user_queries.update_user(uuser.username,uuser.password,uuser.role,user.user_id)
    else:
        uuser.role="user"
        return await user_queries.update_user(uuser.username,uuser.password,uuser.role,user.user_id)





