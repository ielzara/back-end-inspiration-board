from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes: Mapped[int]