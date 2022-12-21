"""Create scripts table

Revision ID: 1deca906082b
Revises: 
Create Date: 2022-12-21 19:38:49.275557

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1deca906082b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "scripts",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=False, start=1, cycle=True),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("game", sa.String(), nullable=True),
        sa.Column("loop", sa.Integer(), nullable=True),
        sa.Column("loop_delay", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scripts_id"), "scripts", ["id"], unique=False)
    op.create_index(op.f("ix_scripts_name"), "scripts", ["name"], unique=True)
    op.create_table(
        "script_actions",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=False, start=1, cycle=True),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("action_type", sa.String(), nullable=True),
        sa.Column("event_type", sa.String(), nullable=True),
        sa.Column("tap_position", sa.String(), nullable=True, comment="x y"),
        sa.Column(
            "swipe_position",
            sa.String(),
            nullable=True,
            comment="swipe from (x_start,y_start) to (x_end y_end): x_start y_start x_end y_end",
        ),
        sa.Column(
            "img_compare_bb",
            sa.String(),
            nullable=True,
            comment="Boudingbox image need to compare: x_start y_start x_end y_end",
        ),
        sa.Column("key_event", sa.String(), nullable=True),
        sa.Column("img", sa.String(), nullable=True, comment="Current Image"),
        sa.Column("loop", sa.Integer(), nullable=True),
        sa.Column("loop_delay", sa.Integer(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("script_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["script_id"],
            ["scripts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_script_actions_id"), "script_actions", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_script_actions_id"), table_name="script_actions")
    op.drop_table("script_actions")
    op.drop_index(op.f("ix_scripts_name"), table_name="scripts")
    op.drop_index(op.f("ix_scripts_id"), table_name="scripts")
    op.drop_table("scripts")
    # ### end Alembic commands ###