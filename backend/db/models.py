from sqlmodel import Field, SQLModel
from datetime import date, datetime


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    surname: str
    email: str
    online_status: bool
    password: str


class FocusLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime
    focus_score: int
    user_id: int = Field(foreign_key="user.id")


class DistractionStat(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: date
    user_id: int = Field(foreign_key="user.id")
    distraction_type: str  # "absent", "looking_away", "multiple_faces"
    count: int = 0
