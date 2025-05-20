from fastapi import FastAPI, APIRouter,  WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from .package.controller import middleware
from fastapi.middleware.cors import CORSMiddleware
from .package.controller.user_router import router as u_router
from .package.controller.book_router import router as b_router
from .package.controller.auth import router as a_router
from .database.dbconn import async_get_db
from os import getenv



app=FastAPI()
router = APIRouter(prefix = "/api", tags = ["auth"])
def async_get_database():
    conn=async_get_db()
    try:
        yield conn
    finally:
        conn.close()
origins=[
    getenv("origin")
]        
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.include_router(u_router)
app.include_router(b_router)
app.include_router(a_router)


manager = middleware.ConnectionManager()

@router.get('/')
async def get():
    return HTMLResponse("index.html")

@router.websocket('/ws/{client_id}')
async def web_socket(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.client_send_message(f'You wrote {data}', websocket)
            await manager.broadcast(f'Client #{client_id} says : {data}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left the chat")
        
        
    
    









    



        
    


    
    