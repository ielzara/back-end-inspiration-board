from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import Optional
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .board import Board

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    count: Mapped[int]

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("board.id"))
    goal: Mapped[Optional["Board"]] = relationship(back_populates="cards")

    def to_dict(self):
        card_dict = {
            "id": self.id,
            "message": self.message,
            "count": self.count,
        }
    
    # Include goal_id if the task belongs to a goal
        if self.board_id is not None:
            card_dict["card_id"] = self.board_id
                
        return card_dict
    
    def to_dict(self):
        card_dict = {
            "id": self.id,
            "message": self.message,
            "count": self.count,
        }
    
    # Include goal_id if the task belongs to a goal
        if self.goal_id is not None:
            card_dict["board_id"] = self.board_id
                
        return card_dict

    @classmethod
    def from_dict(cls, card_data):
        board_id = card_data.get("card_id") 
        new_task = cls(
            message=card_data["message"],
            count=card_data["count"],
            board_id=board_id  
        )

        return new_task