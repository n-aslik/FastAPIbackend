from utils.hash import hashed_password
from package.repository.user_queries import get_user_by_uname_and_password
from package.service import jwt_hand


async def sign_in(username: str, password: str):
    password = await hashed_password(password)
    user = await get_user_by_uname_and_password(username, password)
    if user.get("otp_verify")!="yes":
        return{"otp_verify":"You did not verify OTP"}
    access_token = await jwt_hand.create_access_token(
        user["id"],
        user["username"],
        user["role"],
        user["otp_verify"]
    )
    
    refresh_token=await jwt_hand.create_refresh_token(
        user["id"],
        user["username"],
        user["role"],
        user["otp_verify"]
    )
    return {"access_token":access_token,"refresh_token": refresh_token}






