from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Course, Assignment, File, User, MoodleConnection


def save_course(db: Session, moodle_course: dict, user_id: int) -> Course:

    statement = select(Course).where(Course.moodle_id == moodle_course["id"])
                                    #  Course.user_id == user_id) # Filter by user_id to ensure the course is associated with the correct user
    
    # The statement variable is created using SQLAlchemy's select function to query the Course table for a course with a specific moodle_id that matches the id of the provided moodle_course dictionary. This allows us to check if a course with the same Moodle ID already exists in the database before attempting to save it.
    existing_course = db.scalar(statement)

    if existing_course:
        # If a course with the same Moodle ID already exists in the database, we update its fullname attribute with the new value from the moodle_course dictionary. This ensures that any changes to the course name in Moodle are reflected in our local database.
        existing_course.fullname = moodle_course["fullname"]

        existing_course.user_id = user_id  # Update the user_id to ensure the course is associated with the correct user
        return existing_course

    new_course = Course(
        moodle_id=moodle_course["id"],
        fullname=moodle_course["fullname"],
        user_id = user_id  # Set the user_id for the new course to associate it with the correct user
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


def get_courses_by_user(db: Session, user_id: int) -> list[Course]:
    statement = select(Course).where(Course.user_id == user_id).order_by(Course.id)

    return list(db.scalars(statement).all())


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


def get_user_by_id(db: Session, user_id: int) -> User | None:

    statement = select(User).where(User.id == user_id)

    return db.scalar(statement)


def get_course_by_id_and_user(db: Session, course_id: int, user_id: int) -> Course | None:
    statement = select(Course).where(Course.id == course_id, Course.user_id == user_id)

    return db.scalar(statement)

# Get an assignment by its ID and the associated user ID. This function ensures that the assignment belongs to a course that is associated with the specified user, provided by the user_id parameter. It returns the Assignment object if found, or None if no matching assignment is found.
def get_assignment_by_id_and_user(db: Session, assignment_id: int, user_id: int) -> Assignment | None:
    # The statement variable is created using SQLAlchmy's select function to query the Assignment table for an assignment with a specific ID (assignment_id) that is associated with a course belonging to the specified user (user_id). The join() method is used to join the Assignment table with the Course table based on their relationship defined in the ORM models.
    # The join() method allows us to access the user_id attribute of the Course model, enabling us to filter assignments based on the using the user_id. 
    statement = select(Assignment).join(Course).where(Assignment.id == assignment_id, Course.user_id == user_id)

    return db.scalar(statement)


def get_files_by_assignment(db: Session, assignment_id: int) -> list[File]:

    statement = select(File).where(File.assignment_id == assignment_id)

    return list(db.scalars(statement).all())


def get_moodle_connection_by_user(db: Session, user_id: int) -> MoodleConnection | None:
    statement = select(MoodleConnection).where(MoodleConnection.user_id == user_id)

    return db.scalar(statement)

def save_moodle_connection(db: Session, user_id: int, base_url: str, encrypted_token: str) -> MoodleConnection:
    existing = get_moodle_connection_by_user(db, user_id)

    if existing:
        existing.base_url = base_url
        existing.encrypted_token = encrypted_token

        return existing

    new_connection = MoodleConnection(
        user_id=user_id,
        base_url=base_url,
        encrypted_token=encrypted_token
    )

    db.add(new_connection)
    return new_connection
    
    