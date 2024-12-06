import hashlib
async def hashed_password(password:str)->str:
    return hashlib.sha256(password.encode()).hexdigest()
