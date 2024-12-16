from utils.hash import hashed_password
from package.repository.user_queries import get_user_by_uname_and_password
from package.service.jwt_hand import create_access_token


async def sign_in(username: str, password: str):
    password = await hashed_password(password)
    user = await get_user_by_uname_and_password(username, password)
    access_token = await create_access_token(
        user["id"],
        user["username"],
        user["role"],
        user["otp_veryfied"]
    )
    return {"access_token": access_token}






