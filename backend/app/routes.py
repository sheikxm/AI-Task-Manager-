from fastapi import APIRouter , HTTPException
from typing import List
from app.models import Task , TaskInDB ,TaskInput
from app.crud import create_task , get_tasks , get_task , update_task , delete_task 
from app.genai.BookGen import generate_task_response_logic
router = APIRouter()


@router.get("/tasks", response_model = List[TaskInDB])
async def read_tasks():
    tasks = get_tasks()
    return tasks
@router.get("/tasks/{task_id}" , response_model = TaskInDB)
async def read_task(task_id : str):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code = 404 , detail = "Task Not Found")
    return task 
@router.post("/tasks" , response_model = TaskInDB)
async def create_new_task(task :Task):
    return create_task(task)

@router.put("/tasks/{task_id}", response_model = TaskInDB)
async def update_existing_task(task_id : str , task: Task):
    updated_task = update_task(task_id,task)
    if updated_task is None:
        raise HTTPException(status_code = 404 , detail = "Task Not Found")
    return updated_task
@router.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id : str):
    success = delete_task(task_id)
    if not success:
        raise HTTPException(status_code = 404 , detail = "Task Not Found")
    return {"message" : " Task Deleted"}
@router.post("/tasks/completewithai/")
async def generate_task_response(task_input: TaskInput):
    try:
        # Call the task generation logic
        ai_response = generate_task_response_logic(task_input)
        return {"response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
    
