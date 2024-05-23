from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Tag(Base):
    __tablename__ = "tags"
    name: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(
        secondary="post_tags", back_populates="tags", cascade="all, delete"
    )


class PostTag(Base):
    __tablename__ = "post_tags"

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )
