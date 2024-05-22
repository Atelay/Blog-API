from sqlalchemy.orm import relationship, Mapped

from src.database import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(back_populates="category")
