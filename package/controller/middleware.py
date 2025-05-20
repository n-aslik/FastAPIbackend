from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import HTTPException,Security,status,WebSocketDisconnect, WebSocket
from fastapi.responses import HTMLResponse
from ..service.jwt_hand import parse_token
security=HTTPBearer()


async def checkautherization(sec_route:HTTPAuthorizationCredentials=Security(security)):
    if not sec_route.scheme=="Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid auth scheme")
    token=sec_route.credentials
    pload=await parse_token(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Token is empty")
    if pload.role!="user" and pload.role =="admin":
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    return await parse_token(token)

async def checkautherization_admin_permission(sec_route:HTTPAuthorizationCredentials=Security(security)):
    if not sec_route.scheme=="Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid auth scheme")
    token=sec_route.credentials
    pload=await parse_token(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Token is empty")
    if pload.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    return await parse_token(token)

class ConnectionManager:
    def __init__(self):
        self.active_connections : list[WebSocket] = []
    
    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def client_send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            

        
        
        


       

         


