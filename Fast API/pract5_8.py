"""
#### Задание №8
- Необходимо создать API для управления списком задач. Каждая задача должна
содержать заголовок и описание. Для каждой задачи должна быть возможность
указать статус (выполнена/не выполнена).
- API должен содержать следующие конечные точки:
○ GET /tasks - возвращает список всех задач.
○ GET /tasks/{id} - возвращает задачу с указанным идентификатором.
○ POST /tasks - добавляет новую задачу.
○ PUT /tasks/{id} - обновляет задачу с указанным идентификатором.
○ DELETE /tasks/{id} - удаляет задачу с указанным идентификатором.
- Для каждой конечной точки необходимо проводить валидацию данных запроса и
ответа. Для этого использовать библиотеку Pydantic.
"""
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from starlette.responses import JSONResponse


app = FastAPI()


TASKS: list = []


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: bool


@app.get("/tasks/")
async def all_tasks():
    all_task_dicts = [task.dict() for task in TASKS]
    return JSONResponse(content=all_task_dicts, status_code=200)


@app.get("/task/{id_task}")
async def one_task(id_task: int):

    answer: list = []

    for task_from_list in TASKS:
        if task_from_list.id == id_task:
            answer.append(task_from_list)

    if answer:
        return {"task": answer}
    else:
        return {"error": "Task with this id is not in the database."}


@app.post("/tasks/")
async def create_task(task: Task):

    for task_from_list in TASKS:
        if task_from_list.id == task.id:
            return {"error": "Task with this id already exists"}

    TASKS.append(task)
    return {"add_task": task}


@app.put("/tasks/{id_task}")
async def update_task(task: Task, id_task: int):

    for task_from_list in TASKS:

        if task_from_list.id == id_task:
            task_from_list.title = task.title
            task_from_list.description = task.description
            task_from_list.status = task.status
            return {"change_task": task}

    return {"error": "Task not found"}


@app.delete("/tasks/{id_task}")
async def delete_task(id_task: int):

    count: int = 0

    for task_from_list in TASKS:
        if task_from_list.id == id_task:
            TASKS.pop(count)
            return {"delete_task": task_from_list}
        count += 1
    return {"error": "Task not found"}