import uvicorn
from fastapi import FastAPI, HTTPException
import logging
from models import Task

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tasks = []


@app.get("/tasks/", response_model=list[Task])
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    logger.info(f'Get task: {task_id} done!')
    for i in tasks:
        if i.id == task_id:
            return i
    raise HTTPException(status_code=404, detail="Task not found")


@app.post('/tasks/', response_model=Task)
async def add_task(task: Task):
    logger.info(f'Task {task.id} added')
    for i in tasks:
        if i.id == task.id:
            raise HTTPException(status_code=400, detail=f"Task {task.id} already exist")
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            logger.info(f'Task {task.id} {task.title} updated')
            return tasks[i]

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            logger.info(f'Task {task.id} {task.title} deleted')
            return task
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    uvicorn.run('scheduler:app', host='localhost', port=8000, reload=True)
