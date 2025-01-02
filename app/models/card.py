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
    likes: Mapped[int]

    board_id: Mapped[Optional[int]] = mapped_column(ForeignKey("board.id"))
    board: Mapped[Optional["Board"]] = relationship("Board", back_populates="cards")

    def to_dict(self):
        card_dict = {
            "id": self.id,
            "message": self.message,
            "likes": self.likes,
        }
        if self.board_id is not None:
            card_dict["board_id"] = self.board_id

        return card_dict

    @classmethod
    def from_dict(cls, card_data):
        board_id = card_data.get("board_id")
        new_card = cls(
            message=card_data["message"], likes=card_data["likes"], board_id=board_id
        )

        return new_card
