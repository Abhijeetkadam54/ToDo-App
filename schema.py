from datetime import date
from pydantic import BaseModel
class ToDo(BaseModel):
    id = int
    task = str
    

    class Config:
        orm_mode = True
