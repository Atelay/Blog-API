"""empty message

Revision ID: 61a7f91ffd0f
Revises: 17cfa02e1d10
Create Date: 2024-05-23 13:32:48.673045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "61a7f91ffd0f"
down_revision: Union[str, None] = "17cfa02e1d10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("posts", "author_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("posts", "category_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_constraint("posts_author_id_fkey", "posts", type_="foreignkey")
    op.drop_constraint("posts_category_id_fkey", "posts", type_="foreignkey")
    op.create_foreign_key(
        None, "posts", "authors", ["author_id"], ["id"], ondelete="SET NULL"
    )
    op.create_foreign_key(
        None, "posts", "categories", ["category_id"], ["id"], ondelete="SET NULL"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "posts", type_="foreignkey")
    op.drop_constraint(None, "posts", type_="foreignkey")
    op.create_foreign_key(
        "posts_category_id_fkey", "posts", "categories", ["category_id"], ["id"]
    )
    op.create_foreign_key(
        "posts_author_id_fkey", "posts", "authors", ["author_id"], ["id"]
    )
    op.alter_column("posts", "category_id", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("posts", "author_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###