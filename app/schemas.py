# This file contains the schema definitions for the data structures used in the application. Schemas are used to validate and serialize/deserialize data, ensuring that the data conforms to the expected format

from pydantic import BaseModel
from typing import Optional

class SyncResponse(BaseModel):
    message: str
    downloaded_courses: int
    assignments_processed: int
    files_downloaded: int
    files_already_existing: int


class CourseResponse(BaseModel):
    id: int
    fullname: str


class AssignmentResponse(BaseModel):
    id: int
    name: str
    duedate: int
    intro: Optional[str] = None
    # Optional field for the assignment description, which may not be present in all assignments
    # None is used as the default value to indicate that the field is optional and may be missing in some cases
    