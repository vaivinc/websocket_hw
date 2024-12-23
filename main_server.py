import uvicorn
from fastapi import FastAPI, WebSocket, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect

from routes import route_user, route_auth
from routes.auth import verify_jwt

app = FastAPI(docs_url="/docs")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_chat(request: Request):
    return templates.TemplateResponse(
        request=request, name="websocket_client.html"
    )


# Життєвий Цикл WebSocket-З'єднання:
@app.websocket("/ws/base")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(verify_jwt)):
    try:
        await websocket.accept()
        print(f"User connected: {token}")

        while True:  # Трансфер Даних
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f" Server get message: {data}")

    except WebSocketDisconnect:  # Управління З'єднанням
        print(f"User is disconnected")
    except Exception as e:
        print(f"Critical Error: {e}")

    finally:  # Закриття З'єднання
        if not websocket.client_state.DISCONNECTED:
            await websocket.close()


app.include_router(route_user, prefix="/users", tags=["users"])
app.include_router(route_auth, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
