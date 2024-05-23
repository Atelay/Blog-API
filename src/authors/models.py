from sqlalchemy.orm import relationship, Mapped

from src.database import Base


class Author(Base):
    __tablename__ = "authors"

    name: Mapped[str]
    email: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
