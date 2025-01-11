from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn

app = FastAPI()

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')

socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)


class ConnectionManager:
    def __init__(self):
        self.clients = []

    async def connect(self, sid):
        self.clients.append(sid)

    async def disconnect(self, sid):
        self.clients.remove(sid)

    async def send_messages(self, message):
        await sio.emit('message', {'data':message})


@app.get("/")
def read_root():
    return {"Hello": "World"}

@sio.on("connect")
async def connect(sid, env, auth):
    await sio.emit('message', {'data': f"User joined room {str(sid)}"})

@sio.on('message')
async def handle_message(sid, data):
    await sio.emit('message', {'data': data})

@sio.on("disconnect")
async def disconnect(sid):
    await sio.emit('message', {'data': f"User left room {str(sid)}"})


if __name__ == '__main__':
    uvicorn.run(app)