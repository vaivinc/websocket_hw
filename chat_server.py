import asyncio
import json
import random
from fastapi import WebSocket
from main_server import app
from starlette.websockets import WebSocketDisconnect


active_connections = []


def generate_data():
    stock_data = {
        "Apple": round(random.uniform(140, 150), 2),
        "Google": round(random.uniform(2700, 2800), 2),
        "Amazon": round(random.uniform(3100, 3200), 2)
    }
    new_stock_data = json.dump(stock_data)
    return new_stock_data


@app.websocket("/ws_chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()  # Ініціалізація (Handshake)
    active_connections.append(websocket)
    print("Connect raise")
    try:
        while True:  # Трансфер Даних
            data = generate_data()
            print(data)
            await asyncio.sleep(3)
            for connection in active_connections:
                await connection.send_text(f"{data}")

    except WebSocketDisconnect:  # Управління З'єднанням
        print("Client raise disconnect")

    except Exception as e:
        print(f"Critical Error: {e}")

    finally:  # Закриття З'єднання
        active_connections.remove(websocket)
        if not websocket.client_state.DISCONNECTED:
            await websocket.close()