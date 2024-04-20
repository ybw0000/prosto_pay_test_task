from sqlalchemy.orm import Mapped

from core.base.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str]
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]
