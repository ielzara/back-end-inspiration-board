from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes: Mapped[int]
    board: Mapped[list["Board"]] = relationship(back_populates="board")

    def to_dict(self):
        return {
            "id":self.id,
            "message":self.message,
            "likes": self.likes
        }
    
        @classmethod
        def from_dict(cls, card_data):
            new_card = cls(message=card_data["message"])
            return new_card