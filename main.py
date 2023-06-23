from fastapi import FastAPI,Request,Depends,Form,HTTPException
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
import schema
from dbconn import SessionLocal, engine
import model
from model import ToDo
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
model.Base.metadata.create_all(bind=engine) #for creating tables bindinf db engine

# Function to create and close the session in all of our routes
def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


#  decorator to define the routing of the root function
@app.get("/")

#function To get all task 
async def allTask(request: Request,db: Session = Depends(get_database_session)):

    with open('database.json') as f:
        
        data = db.query(ToDo).all()
        
    
    return templates.TemplateResponse("todolist.html",{"request":request,"tododict":data})

# Function to get a single task
@app.get("/task/{name}")
def get_task(request: Request, name: schema.ToDo.task, db: Session = Depends(get_database_session)):
    
    item = db.query(ToDo).filter(ToDo.task==name).first()
    print(item.task)
    return templates.TemplateResponse("todo.html", {"request": request, "task": item})


# Function to update a task
@app.post("/update")
async def update_todo(request: Request,task:schema.ToDo.task=Form(...),id:schema.ToDo.id=Form(...),db: Session = Depends(get_database_session)):
    try:
        print(task,id)
        TasktoUpdate = db.query(ToDo).get(id)
        TasktoUpdate.task=task
        db.commit()
        db.refresh(TasktoUpdate)
        return RedirectResponse("/", 303)
    except Exception as e:
        print(e)    
        raise HTTPException(status_code=404, detail="something happened")


# Function to delete task
@app.get("/delete/{id}")
async def delete_todo(request: Request, id: str,db: Session = Depends(get_database_session)):
    try:
        print(id)
        taskToDelete = db.query(ToDo).get(id)
        db.delete(taskToDelete)
        db.commit()
        return RedirectResponse("/", 303)
    except Exception as e:
        print(e)    
        raise HTTPException(status_code=404, detail="something happened")



@app.post("/add")
async def add_todo(request: Request,db: Session = Depends(get_database_session),task:schema.ToDo.task=Form(...)):
    newTask=ToDo(task=task)
    db.add(newTask)
    db.commit()
    return RedirectResponse("/", 303)