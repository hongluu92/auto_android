"""init

Revision ID: ba84b27700a7
Revises: 
Create Date: 2022-12-28 20:00:27.973868

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ba84b27700a7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "actions",
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
        sa.Column("is_click_all_image", sa.Boolean(), nullable=True),
        sa.Column("key_event", sa.String(), nullable=True),
        sa.Column("img", sa.String(), nullable=True, comment="Current Image"),
        sa.Column("loop", sa.Integer(), nullable=True),
        sa.Column("loop_delay", sa.Integer(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.Column("scale", sa.Float(), nullable=True),
        sa.Column("image_compare_threshhold", sa.Float(), nullable=True),
        sa.Column("new_thread", sa.Boolean(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_actions_id"), "actions", ["id"], unique=False)
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
        "action_refs",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=False, start=1, cycle=True),
            nullable=False,
        ),
        sa.Column("child_id", sa.Integer(), nullable=False),
        sa.Column("parrent_id", sa.Integer(), nullable=True),
        sa.Column("loop", sa.Integer(), nullable=True),
        sa.Column("loop_delay", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["child_id"],
            ["actions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["parrent_id"],
            ["actions.id"],
        ),
        sa.PrimaryKeyConstraint("id", "child_id", "parrent_id"),
    )
    op.create_index(
        op.f("ix_action_refs_child_id"), "action_refs", ["child_id"], unique=False
    )
    op.create_index(op.f("ix_action_refs_id"), "action_refs", ["id"], unique=False)
    op.create_index(
        op.f("ix_action_refs_parrent_id"), "action_refs", ["parrent_id"], unique=False
    )
    op.create_table(
        "script_actions",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=False, start=1, cycle=True),
            nullable=False,
        ),
        sa.Column("script_id", sa.Integer(), nullable=False),
        sa.Column("action_id", sa.Integer(), nullable=False),
        sa.Column("loop", sa.Integer(), nullable=True),
        sa.Column("loop_delay", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["action_id"],
            ["actions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["script_id"],
            ["scripts.id"],
        ),
        sa.PrimaryKeyConstraint("id", "script_id", "action_id"),
    )
    op.create_index(
        op.f("ix_script_actions_action_id"),
        "script_actions",
        ["action_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_actions_id"), "script_actions", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_script_actions_script_id"),
        "script_actions",
        ["script_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_script_actions_script_id"), table_name="script_actions")
    op.drop_index(op.f("ix_script_actions_id"), table_name="script_actions")
    op.drop_index(op.f("ix_script_actions_action_id"), table_name="script_actions")
    op.drop_table("script_actions")
    op.drop_index(op.f("ix_action_refs_parrent_id"), table_name="action_refs")
    op.drop_index(op.f("ix_action_refs_id"), table_name="action_refs")
    op.drop_index(op.f("ix_action_refs_child_id"), table_name="action_refs")
    op.drop_table("action_refs")
    op.drop_index(op.f("ix_scripts_name"), table_name="scripts")
    op.drop_index(op.f("ix_scripts_id"), table_name="scripts")
    op.drop_table("scripts")
    op.drop_index(op.f("ix_actions_id"), table_name="actions")
    op.drop_table("actions")
    # ### end Alembic commands ###
