"""
#### Задание №5
- Создать API для удаления информации о пользователе из базы данных.
Приложение должно иметь возможность принимать DELETE запросы и
удалять информацию о пользователе из базы данных.
- Создайте модуль приложения и настройте сервер и маршрутизацию.
- Создайте класс User с полями id, name, email и password.
- Создайте список users для хранения пользователей.
- Создайте маршрут для удаления информации о пользователе (метод DELETE).
- Реализуйте проверку наличия пользователя в списке и удаление его из
списка.
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


@app.delete("/delete_user/")
async def delete_user(user: User):

    sequence_number: int = -1

    for number_task in range(len(USERS)):

        if USERS[number_task].id == user.id:
            sequence_number = number_task

    if sequence_number < 0:
        return {"error": "user not found"}
    else:
        USERS.pop(sequence_number)
        return {"delete_task": user}



