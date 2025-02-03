from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Request
import socketio
import uvicorn
from database import users, get_session, get_session_fa, Message
from pydantic import BaseModel
import jwt
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

SECRET_KEY = 'KEY'
ALGORITHM = 'HS256'

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')

socket_app = socketio.ASGIApp(sio, app)

templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.clients = {}

    async def connect(self, data):
        self.clients[data['sid']] = data['user']
        await sio.emit('sysmessage', {'data': f"User {data['user']} joined room"})

    async def disconnect(self, sid):
        user = self.clients[sid]
        del self.clients[sid]
        await sio.emit('sysmessage', {'data': f"User {user} left room"})

    async def send_messages(self, sid, message):
        ts = datetime.now()
        with get_session() as db:
            m = Message(
                send_time=ts,
                sender=self.clients[sid],
                message=message
            )
            db.add(m)
            db.commit()
            db.refresh(m)
        await sio.emit('message', {"id": m.id, 'message':message, 'from': self.clients[sid], 'ts': ts.strftime('%Y-%m-%d %H:%M')})



cm = ConnectionManager()


class User(BaseModel):
    username: str
    password: str

def authenticate_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        for user in users:
            if user['token'] == token:
                return True
    except:
        return False


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/users/")
def get_users(token: str):
    if not authenticate_user(token):
        raise HTTPException(401, detail="Unauthorized")
    return [x for x in cm.clients.values()]


@app.post("/add_user/")
def add_user(user: User, token: str):
    if not authenticate_user(token):
        raise HTTPException(401, detail="Unauthorized")
    for user_db in users:
        if user_db['login'] == user.username:
            raise HTTPException(400, detail="Already exists")
    users.append({
        "login": user.username,
        "password": user.password,
        "token": None
    })


@app.get("/remove_user/")
def remove_user(user: str, token: str):
    if not authenticate_user(token):
        raise HTTPException(401, detail="Unauthorized")
    for user_db in users:
        if user_db['login'] == user:
            users.remove(user_db)
            return "OK"


@app.post("/login/")
def login(user: User):
    for user_db in users:
        if user_db['login'] == user.username and user_db['password'] == user.password:
            expire = datetime.now() + timedelta(hours=12)
            encoded_jwt = jwt.encode({"user": user.username, 'exp': expire}, SECRET_KEY, algorithm=ALGORITHM)
            user_db['token'] = encoded_jwt
            return encoded_jwt
    raise HTTPException(401, detail='Unauthorized')

@app.get("/history/")
def get_history(day: datetime, token: str, db = Depends(get_session_fa)):
    if not authenticate_user(token):
        raise HTTPException(401, detail="Unauthorized")
    return db.query(Message).filter(Message.send_time >= day-timedelta(hours=24)).all()


@sio.on("connect")
async def connect(sid, env, auth):
    if not authenticate_user(auth):
        return False#raise ConnectionRefusedError('authentication failed')
    for user in users:
        if user['token'] == auth:
            await cm.connect({"sid": sid, "user": user['login']})
            break
    else:
        return False# raise ConnectionRefusedError('authentication failed')


@sio.on('message')
async def handle_message(sid, data):
    if data is None or data == '':
        return
    await cm.send_messages(sid, data)


@sio.on("disconnect")
async def disconnect(sid, reason):
    await cm.disconnect(sid)


if __name__ == '__main__':
    uvicorn.run(socket_app)