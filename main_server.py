import uvicorn
from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect

from routes import route_user, route_auth

app = FastAPI(docs_url="/docs")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_chat(request: Request):
    return templates.TemplateResponse(
        request=request, name="websocket_client.html"
    )


# Життєвий Цикл WebSocket-З'єднання:
@app.websocket("/ws/base")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Ініціалізація (Handshake)
    print("Connect raise")
    try:
        while True:  # Трансфер Даних
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f" Server get message: {data}")

    except WebSocketDisconnect:  # Управління З'єднанням
        print("Client raise disconnect")
    except Exception as e:
        print(f"Critical Error: {e}")

    finally:  # Закриття З'єднання
        if not websocket.client_state.DISCONNECTED:
            await websocket.close()


app.include_router(route_user, prefix="/users", tags=["users"])
app.include_router(route_auth, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)