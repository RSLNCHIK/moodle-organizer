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

    # back_populates is used to define a bidirectional relationship between the Assignment and File models. It allows us to access the related files for an assignment and vice versa. The back_populates parameter specifies the attribute name in the related model that coresponds to this relationship. In this case, it indicates that the files attribute in the Assignment model is related to the assignment attribute in the File model.
    files: Mapped[list["File"]] = relationship(back_populates="assignment")

class File(Base):

    __tablename__="files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    filename: Mapped[str] = mapped_column(String, nullable=False)

    # The mimetype attribute is a string that represents the MIME type of the file (e.g., "application/pdf", "image/png"). It is optional and can be null in the database.
    mimetype: Mapped[str | None] = mapped_column(String, nullable=True)

    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"), nullable=False)

    assignment: Mapped["Assignment"] = relationship(back_populates="files")
    
class User(Base):
    __tablename__ = "users"

    # Mapped is a type hint provided by SQLAlchemy that indicates that the attribute is mapped to a column in the database table. It allows for better type checking and code completion in IDEs.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    

