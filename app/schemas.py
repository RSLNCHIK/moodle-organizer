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
    moodle_id: int
    fullname: str

    # The model_config dictionary is used to configure the behavior of the Pydantic model. In this case, it specifies that the model should be populated from attributes, allowing for more flexible data handling and validation.
    model_config = {
        "from_attributes": True
    }


class AssignmentResponse(BaseModel):
    id: int
    name: str
    duedate: int
    intro: Optional[str] = None
    # Optional field for the assignment description, which may not be present in all assignments
    # None is used as the default value to indicate that the field is optional and may be missing in some cases
    