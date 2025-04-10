from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket

connections = []


async def hello(request):
    return JSONResponse({"hello": "world"})


async def ping(request):
    for c in connections:
        await c.send_text("pong")
    return JSONResponse({"status": "ok"})


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, world!")
    await websocket.close()


async def websocket_register(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)


app = Starlette(
    debug=True,
    routes=[
        Route("/hello", hello, methods=["GET", "POST"]),
        Route("/ping", ping, methods=["POST"]),
        WebSocketRoute("/ws/hello", websocket_endpoint),
        WebSocketRoute("/ws/register", websocket_register),
    ],
)
