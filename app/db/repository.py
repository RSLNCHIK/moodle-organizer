from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Course, Assignment


def save_course(db: Session, moodle_course: dict):

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

def save_assignment(db: Session, moodle_assignment: dict, course: Course):
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




