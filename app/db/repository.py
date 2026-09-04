from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Course, Assignment, File, User


def save_course(db: Session, moodle_course: dict) -> Course:

    statement = select(Course).where(Course.moodle_id == moodle_course["id"])
    # The statement variable is created using SQLAlchemy's select function to query the Course table for a course with a specific moodle_id that matches the id of the provided moodle_course dictionary. This allows us to check if a course with the same Moodle ID already exists in the database before attempting to save it.
    existing_course = db.scalar(statement)

    if existing_course:
        # If a course with the same Moodle ID already exists in the database, we update its fullname attribute with the new value from the moodle_course dictionary. This ensures that any changes to the course name in Moodle are reflected in our local database.
        existing_course.fullname = moodle_course["fullname"]
        return existing_course

    new_course = Course(
        moodle_id=moodle_course["id"],
        fullname=moodle_course["fullname"]
    )

    db.add(new_course)
    return new_course

def save_assignment(db: Session, moodle_assignment: dict, course: Course) -> Assignment:
    statement = select(Assignment).where(Assignment.moodle_id == moodle_assignment["id"])

    existing_assignment = db.scalar(statement)

    if existing_assignment:
        existing_assignment.name = moodle_assignment["name"]
        existing_assignment.duedate = moodle_assignment.get("duedate", "Keine Fälligkeit")
        existing_assignment.course_id = course.id
        return existing_assignment

    new_assignment = Assignment(
        moodle_id=moodle_assignment["id"],
        name=moodle_assignment["name"],
        duedate=moodle_assignment.get("duedate", "Keine Fälligkeit"),
        course_id=course.id
    )

    db.add(new_assignment)
    return new_assignment


def get_all_courses(db: Session):
    statement = select(Course)
    return db.scalars(statement).all()


def get_all_assignments_by_course(db: Session, course_id: int) -> list[Assignment]:
    statement = select(Assignment).where(Assignment.course_id == course_id)
    # The statement variable is created using SQLAlchemy's select function to query the Assignment table for all assignments that belong to a specific course, identified by the provided course_id. This allows us to retrieve all assignments associated with a particular course from the database.
    # scalars() is a method provided by SQLAlchmy that executes the query and returns an iterable of scalar values (in this case, Assignment objects) instead of full row objects. This is useful when we only need the mapped objects and not the entire row data. Mapped objects are instances of the ORM model classes (like Assignment) that represent rows in the databese tables. They allow us to work with the data in a more Pydantic and object-oriented way, rather than dealing with raw database rows. The all() method is then called on the result of scalars() to retrieve all the matching Assignment objects as a list, which can be easily used in the application.
    return list(db.scalars(statement).all())



def get_course_by_id(db: Session, course_id: int) -> Course | None:
    statement = select(Course).where(Course.id == course_id)
    return db.scalar(statement)


def save_file(db: Session, moodle_file: dict, assignment: Assignment) -> File:
    statement = select(File).where(File.assignment_id == assignment.id, File.filename == moodle_file["filename"])

    existing_file = db.scalar(statement)

    if existing_file:
        return existing_file

    new_file = File(
        filename=moodle_file["filename"],
        mimetype=moodle_file.get("mimetype"),
        assignment_id=assignment.id
    )

    db.add(new_file)
    return new_file


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)

    return db.scalar(statement)

def create_user(db: Session, email: str, hashed_password: str) -> User:
    # create a new user instance with the provided email and hashed password. The User model is used to reprsent the user data in the database, and the new_user object is created with the specified email and hashed password. This object will be added to the database session for persistence.
    new_user = User(
        email=email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()  # Commit the transaction to save the new user to the database
    db.refresh(new_user)  # Refresh the new_user instance to get the updated data from the database (e.g., auto-generated ID)
    return new_user