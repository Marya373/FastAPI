"""
#### Задание №6
- Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
- Создайте модуль приложения и настройте сервер и маршрутизацию.
- Создайте класс User с полями id, name, email и password.
- Создайте список users для хранения пользователей.
- Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
- Создайте маршрут для отображения списка пользователей (метод GET).
- Реализуйте вывод списка пользователей через шаблонизатор Jinja.
"""
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


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


@app.get("/add_user_html/", response_class=HTMLResponse)
async def add_user_html(request: Request):
    page_title: str = 'Добавить пользователя'
    return templates.TemplateResponse("practice_5_task_6_add_user.html",
                                      {
                                          "request": request,
                                          "page_title": page_title,
                                      })


@app.post("/add_user_html_post/")
async def add_user_html_post(
                name: str = Form(default=" * ", alias="name"),
                email: str = Form(default=" * ", alias="email"),
                password: str = Form(default=" * ", alias="password")
):

    id = USERS[len(USERS)-1].id + 1

    USERS.append({
        "id": id,
        "name": name,
        "email": email,
        "password": password
    })

    return {"message": "User registered successfully"}


@app.get("/get_all_user/", response_class=HTMLResponse)
async def get_all_user(request: Request):

    page_title: str = 'Все пользователи'

    return templates.TemplateResponse("practice_5_task_6.html",
                                      {
                                          "request": request,
                                          "page_title": page_title,
                                          "users": USERS
                                      })


@app.get("/get_all_user_jason/")
async def get_all_user():
    return {"all_users_in_jason": USERS}


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
        return {"error": "User not found"}
    else:
        USERS.pop(sequence_number)
        return {"delete_task": user}
