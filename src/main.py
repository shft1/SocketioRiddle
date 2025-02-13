import random

import eventlet
import socketio
from eventlet import wsgi
from loguru import logger

from src.all_riddles import riddles

# Заставляем работать пути к статике
static_files = {"/": "static/index.html", "/static": "./static"}
sio = socketio.Server(cors_allowed_origins="*", async_mode="eventlet")
app = socketio.WSGIApp(sio, static_files=static_files)


session = {}


class Player:
    def __init__(self):
        self.user_riddles = []
        self.steps = 0
        self.count = 0

    def take_riddle(self):
        self.steps += 1
        new_riddle = random.choice(riddles)
        while new_riddle in self.user_riddles:
            new_riddle = random.choice(riddles)
        self.user_riddles.append(new_riddle)
        return new_riddle

    def check_answer(self, answer):
        if answer == self.user_riddles[-1]["answer"]:
            self.count += 1
            return True
        else:
            self.count -= 1

    def check_finish(self):
        if self.steps == len(riddles):
            self.steps = 0
            self.user_riddles = []
            self.count = 0
            return True


# Обрабатываем подключение пользователя
@sio.event
def connect(sid, environ):
    session[sid] = Player()
    logger.info(f"Пользователь {sid} подключился")


# Обрабатываем запрос очередного вопроса
@sio.on("next")
def next_event(sid, data):
    player = session[sid]
    if player.check_finish():
        sio.emit("over")
    else:
        next_riddle = player.take_riddle()
        sio.emit("riddle", data={"text": next_riddle["text"]})


# Обрабатываем отправку ответа
@sio.on("answer")
def receive_answer(sid, data):
    player = session[sid]
    player_riddle = player.user_riddles[-1]
    sio.emit(
        "result",
        data={
            "riddle": player_riddle["text"],
            "is_correct": player.check_answer(data["text"]) is True,
            "answer": player_riddle["answer"],
        },
    )
    sio.emit("score", data={"value": player.count})


# Обрабатываем отключение пользователя
@sio.event
def disconnect(sid):
    session.pop(sid, "Пользоваетель не был в игре!")
    logger.info(f"Пользователь {sid} отключился")


if __name__ == "__main__":
    wsgi.server(eventlet.listen(("127.0.0.1", 8000)), app)
