"""initial schema

Revision ID: 6ffbaa4e9085
Revises: 
Create Date: 2026-09-15 14:50:43.917118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ffbaa4e9085'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # sa is an alias for the SQLAlchemy library, which is used to define the database schema.
    # op is an alias for the Alembic operations module, which is used to perform database schema migrations.
    # The create_table function is used to create a new table in the database
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"))

    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("moodle_id", sa.Integer(), nullable=False),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("moodle_id"))

    # UniqueConstraint is added to ensure that each assignment has a unique moodle_id.
    # ForeignKeyConstraint is added to establish a relationship between assignments and courses.
    # The assignments table has a foreign key constraint on course_id that references the id column in the courses table.
    # moodle_id is a unique identifier for assignments in Moodle, and it is important to ensure that each assignment has a unique moodle_id to avoid conflicts and maintain data integrity.
    # course_id is a foreign key that establishes a relationship between assignments and courses, allowing us to associate each assignment with a specific course.
    # moodle_id can be used to identify assignments in Moodle, while course_id can be used to identify the course to which the assignment belongs.
    # moodle_id is unique to each assignment, while course_id can be shared by multiple assignments that belong to the same course.
    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("moodle_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("duedate", sa.Integer(), nullable=True),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
        sa.PrimaryKeyConstraint("id"), 
        sa.UniqueConstraint("moodle_id"))

    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("mimetype", sa.String(), nullable=True),
        sa.Column("assignment_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["assignment_id"], ["assignments.id"]),
        sa.PrimaryKeyConstraint("id"))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the tables in reverse order of creation to avoid foreign key constraint issues.
    # The files table is dropped first because it has a foreign key constraint on the assignments table.
    # The assignments table is dropped next because it has a foreign key constraint on the courses table.
    # The courses table is dropped next because it has a foreign key constraint on the users table.
    # The users table is dropped last.
    op.drop_table("files")
    op.drop_table("assignments")
    op.drop_table("courses")
    op.drop_table("users")
