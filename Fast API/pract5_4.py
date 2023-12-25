"""
#### Задание №4
- Создать API для обновления информации о пользователе в базе данных.
Приложение должно иметь возможность принимать PUT запросы с данными
пользователей и обновлять их в базе данных.
- Создайте модуль приложения и настройте сервер и маршрутизацию.
- Создайте класс User с полями id, name, email и password.
- Создайте список users для хранения пользователей.
- Создайте маршрут для обновления информации о пользователе (метод PUT).
- Реализуйте валидацию данных запроса и ответа.
"""
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


USERS: list = []


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


@app.post("/add_user/")
async def add_user(user: User):

    for user_from_list in USERS:
        if user_from_list.id == user.id:
            return {"error": "User with this id is already in the database."}

    USERS.append(user)
    return {"add_user": user}


@app.get("/get_user/{user_id}")
async def get_user(user_id: int):

    answer: list = []

    for user_from_list in USERS:
        if user_from_list.id == user_id:
            answer.append(user_from_list)

    if answer:
        return {"user": answer}
    else:
        return {"error": "User with this id is not in the database."}


@app.put("/update_user_data/")
async def update_user_data(user: User):

    for user_from_list in USERS:

        if user_from_list.id == user.id:
            user_from_list.name = user.name
            user_from_list.email = user.email
            user_from_list.password = user.password

            return {"update_user_data": user}

    return {"error": "User not found"}
