import asyncio
import websockets
from aioconsole import ainput, aprint
from fastapi import Depends

from routes.auth import oauth2_scheme


async def websocket_client_chat(username: str, token: str = Depends(oauth2_scheme)):
    uri = "ws://localhost:8000/ws/base"
    try:
        async with websockets.connect(uri, open_timeout=None) as websocket:
            print("Соединение установлено!")

            async def send_message():
                while True:
                    message = await ainput("->: ")
                    if message.lower() == "exit":
                        await websocket.send(f"{username} exit from chat")
                        await websocket.close()
                    await websocket.send(f"{username}: {message}")

            async def recive_message():
                while True:
                    try:
                        response = await websocket.recv()
                        await aprint(f"\r{response}\n->: ", end="")

                    except websockets.exceptions.ConnectionClosed:
                        print("Server close connect")
                        break

            await asyncio.gather(send_message(), recive_message())

    except Exception as e:
        print(f"Ошибка {e}")


if __name__ == "__main__":
    username = input("Enter your name: ")
    token = input("Enter your token: ")
    asyncio.run(websocket_client_chat(username, token))
