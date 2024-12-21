import asyncio
import websockets


async def websocket_client():
    uri = "ws://localhost:8000/ws/base"
    try:
        async with websockets.connect(uri, open_timeout=None) as websocket:
            print("Соединение установлено!")

            while True:
                print("-" * 25)
                message = input("Введите message or 'exit' для выхода): ")
                if message.lower() == "exit":
                    print("Закрытие соединения...")
                    break

                await websocket.send(message)
                print(f"Сообщение отправлено: {message}")

                response = await websocket.recv()
                print(f"Ответ от сервера: {response}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Соединение закрыто: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(websocket_client())