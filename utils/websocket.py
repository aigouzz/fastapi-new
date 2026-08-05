from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import random

router = APIRouter()
connections_chat: list[WebSocket] = []

@router.websocket("/ws2")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try: 
        while True:
            data = await websocket.receive_text()
            number = random.random()
            await websocket.send_text("%.2f"%number)
    except WebSocketDisconnect as wsdc:
        print(f"{websocket} 断开连接")

@router.websocket("/ws2/{name}")
async def ws_all(websocket: WebSocket, name: str):
    await websocket.accept()
    connections_chat.append(websocket)
    await websocket.send_text(f"{name}, 你已经进入聊天室，可以聊天了")
    for client in connections_chat:
        if client != websocket:
            await client.send_text(f"{name}进入聊天")
    try: 
        while True:
            data = await websocket.receive_text()
            for client in connections_chat:
                await client.send_text(f"{name}说：{data}")
            # number = random.random()
            # await websocket.send_text("%.2f"%number)
    except WebSocketDisconnect as wsdc:
        print(f"{websocket} 断开连接")
        connections_chat.remove(websocket)
        for client in connections_chat:
            await client.send_text(f"{name}退出了聊天")