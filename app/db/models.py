from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Course(Base):
    __tablename__ = "courses"


    # The Course class represents a course in the database. It inherits from the Base class, which is a declarative base provided by SQLAlchemy. The __tablename__ attribute specifies the name of the table in the database that corresponds to this model.
    # id is the primary key for the Course table, which is an integer that uniquely identifies each course in the database.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # The moodle_id attribute is a unique integer that corresponds to the course ID in Moodle.
    # nullable=False means that this field cannot be left empty when creating a new course record in the database.
    # Mapped[int] indicates that this attribute is mapped to a column in the database table and is of type integer.
    moodle_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    fullname: Mapped[str] = mapped_column(String, nullable=False)

    assignments: Mapped[list["Assignment"]] = relationship(back_populates="course")


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    moodle_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)

    duedate: Mapped[int] = mapped_column(Integer, nullable=False)

    # The course_id attribute is a foreign key that references the id column in the courses table. This establishes a relationship between the Assignment and Course models.
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    course: Mapped["Course"] = relationship(back_populates="assignments")

    
