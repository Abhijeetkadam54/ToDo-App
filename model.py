from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from dbconn import Base
class ToDo(Base):
    __tablename__ = "ToDo"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(20), unique=True)
    