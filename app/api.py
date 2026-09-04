import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from .services.downloader import download_assignment_files
from .services.auth_service import hash_password
from .schemas import SyncResponse, CourseResponse, AssignmentResponse, UserCreate, UserResponse
from .db.database import SessionLocal
from .db.repository import (save_course, 
                            save_assignment, 
                            get_all_courses, 
                            get_all_assignments_by_course, 
                            get_course_by_id, 
                            save_file,
                            get_user_by_email,
                            create_user
                            )
from .db.models import Course, Assignment

from .clients.moodle_client import (
    get_site_info,
    get_courses,
    get_assignments
)
# Load environment variables from .env file

load_dotenv()

MOODLE_URL = os.getenv("MOODLE_URL")
TOKEN = os.getenv("MOODLE_TOKEN")

url = f"{MOODLE_URL}/webservice/rest/server.php"


app = FastAPI()

# This is the main endpoint for Moodle's web service API
# Through this endpoint (URL) we can make requests to various Moodle functionss

@app.get("/")
def root():
    return {"message": "Moodle Organizer API läuft!"}

# This endpoint retrieves the list of courses for the authenticated user

# the response_model parameter specifies the expected response format for the endpoint. In this case, it expectes a response that matches the CourseResponse schema defined in app/schemas.py. This allows FastAPI to automatically validate and serialize the response data according to the defined schema.
@app.get("/courses", response_model=list[CourseResponse])
def get_user_courses():

    with SessionLocal() as db:
        # Retrieve all courses from the database using the get_all_courses function, which queries the Course table and returns a list of Course objects. This allows us to fetch the courses that have been previously saved in the local database.
        courses = get_all_courses(db)

        return courses

@app.get("/courses/{course_id}/assignments", response_model=list[AssignmentResponse])
def course_assignments(course_id: int):

    # The course_id parameter is used to identify the specific course for which to retrieve assignments.
    # The get_all_assignments_by_course function is called with the database session and the course ID to fetch all assignments associated with that course.
    
    with SessionLocal() as db:


        course = get_course_by_id(db, course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Kurs nicht gefunden :(")
        
        assignments = get_all_assignments_by_course(db, course_id)

    return assignments

    # assignments_data["courses"]
    # → Liste der zurückgegebenen Kurse

    # assignments_data["courses"][0]
    # → erster/bei uns einziger Kurs

    # assignments_data["courses"][0]["assignments"]
    # → Aufgaben dieses Kurses

    # assignments_data = get_assignments(url, TOKEN, [selected_course])
    

# The response_model parameter specifies the expected response format for the endpoint. In this case, it expects a response that matches the SyncResponse schema defined in app/schemas.py. This allows FastAPI to automatically validate and serialize the response data according to the defined schema.

@app.post("/sync", response_model=SyncResponse)
def sync_moodle():
    site_info = get_site_info(url, TOKEN)

    user_id = site_info["userid"]

    moodle_courses = get_courses(url, TOKEN, user_id)

    assignments_data = get_assignments(url, TOKEN, moodle_courses)


    downloaded_courses = 0
    processed_assignments = 0
    files_downloaded = 0
    files_skipped = 0
    

    # Save courses to the database
    # The with statement is used to create a context manager for the database session. This ensures that the session is properly closed after the block of code is executed, even if an exception occurs. The SessionLocal() function is called to create a new database session, which is then used to save the courses retrieved from Moodle into the local database using the save_course function. After all courses have been processed, db.commit() is called to persist the changes to the database.
    with SessionLocal() as db:


        saved_courses: dict[int, Course] = {}

        for moodle_course in moodle_courses:
            db_course = save_course(db, moodle_course)

            # The saved_courses dictionary is used to keep track of the courses that have been saved to the database. The key is the Moodle course ID, and the value is the corresponding Course object from the database. This allows us to easily reference the saved courses later when saving assignments, ensuring that each assignment is associated with the correct course in the database.
            saved_courses[moodle_course["id"]] = db_course

        db.flush()  # Flush the session to generate IDs for new courses

        for moodle_course in assignments_data["courses"]:
            moodle_course_id = moodle_course["id"]

            # The moodle_course_id is the ID of the current Moodle course being processed. We use this ID to look up the corresponding Course object in the saved_courses dictionary, which contains all the courses that have been saved to the database.
            db_course = saved_courses[moodle_course_id]

            downloaded_courses += 1

            for assignment in moodle_course["assignments"]:

                processed_assignments += 1

                db_assignments = save_assignment(db, assignment, db_course)

                db.flush()  # Flush the session to generate IDs for new assignments

                attachments = assignment.get("introattachments", [])


                for moodle_file in attachments:
                    save_file(db, moodle_file, db_assignments)


            # The files download (local)

            # downloaded, skipped = download_assignment_files(
            #         assignment,
            #         TOKEN,
            #         moodle_course["fullname"]
            #     )

            # files_downloaded += downloaded
            # files_skipped += skipped


        db.commit()  # Commit the changes to the database


    return {
            "message": "Synchronisierung abgeschlossen!",
            "downloaded_courses": downloaded_courses,
            "assignments_processed": processed_assignments,
            "files_downloaded": files_downloaded,
            "files_already_existing": files_skipped
        }


@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate):
    with SessionLocal() as db:
        existing_user = get_user_by_email(db, user.email)

        if existing_user:
            raise HTTPException(status_code=409, detail="Benutzer mit dieser E-Mail existiert bereits.")

        hashed_password = hash_password(user.password)

        new_user = create_user(db, user.email, hashed_password)

        db.commit()  # Commit the transaction to save the new user to the database
        db.refresh(new_user)  # Refresh the new_user instance to get the updated data from the database

        return new_user