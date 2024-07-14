from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Column, Integer, DateTime
import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id = mapped_column(ForeignKey("user.id"))
    recipient_id = mapped_column(ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    message: Mapped[str] = mapped_column(String(1024))

    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, sender_id={self.sender_id!r}, recipient_id={self.receipient_id!r}, timestamp={self.timestamp!r}, message={self.message!r}"