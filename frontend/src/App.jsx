import { useEffect, useState } from "react";
import CourseList from "./components/CourseList";
import Navbar from "./components/Navbar";
import LoginForm from "./components/LoginForm";
import AssignmentList from "./components/AssignmentList";
import FileList from "./components/FileList";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");

  const [selectedCourse, setSelectedCourse] = useState(null);
  const [assignments, setAssignments] = useState([]);

  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [files, setFiles] = useState([]);
  

  async function handleLogin(event) {
    event.preventDefault();

    setError("");

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch(
      "http://127.0.0.1:8000/login",
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
        },
        body: formData,
      }
    );

    if (!response.ok) {
      setError("Login fehlgeschlagen");
      return;
    }

    const data = await response.json();

    localStorage.setItem(
      "access_token",
      data.access_token
    );

    setToken(data.access_token);
  }

  async function loadCourses(currentToken) {
    const response = await fetch(
      "http://127.0.0.1:8000/courses",
      {
        headers: {
          Authorization: `Bearer ${currentToken}`,
        },
      }
    );

    if (!response.ok) {
      return;
    }

    const data = await response.json();
    setCourses(data);
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    setToken(null);
    setCourses([]);
  }

  // ${token} comes from the state variable token, which is set when the user logs in. It is used to authenticate the request to the backend API.
  // loadAssignments takes a ${token} from the localStorage
  async function loadAssignments(courseId) {
    const response = await fetch(`http://127.0.0.1:8000/courses/${courseId}/assignments`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      }
    });

    if(!response.ok) {
      console.log("Fehler beim Laden der Aufgaben");
      return;

    }

    const data = await response.json();

    setAssignments(data);
    setSelectedCourse(courseId);

  }

  // await is used to wait for the response from the backend API before continuing with the execution of the code. 
  // This is important because we need to wait for the data to be loaded before we can set the state variables files and selectedAssignment.
  async function loadFiles(assignmentId) {
    const response = await fetch(`http://127.0.0.1:8000/assignments/${assignmentId}/files`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`

      }
    });

    if (!response.ok) {
      console.log("Fehler beim Laden der Datein");
      return;

    }

    const data = await response.json();

    // setFiles is used to set the state variable files with the data received from the backend API. This is used to display the files in the frontend.
    // setSelectedAssignment is used to set the state variable selectedAssignment with the assignmentId received from the backend API. This is used to display the files of the selected assignment in the frontend.
    setFiles(data);
    setSelectedAssignment(assignmentId);

  }

  // UseEffect is a React hook that allows to perform side effects in function components. In this case, it is used to load the courses when the token changes.
  useEffect(() => {
    if (token) {
      loadCourses(token);
    }
  }, [token]);

  return (
    <div className="min-h-screen bg-gray-100">
      {!token ? (
        <LoginForm
          email={email}
          setEmail={setEmail}
          password={password}
          setPassword={setPassword}
          handleLogin={handleLogin}
          error={error}
        />
      ) : (
        // p-8 is used to add padding of 2 rem (32px) to all sides of the cotainer.
        // mb-3 is used to add a margin-bottom of 0.75 rem (12px) to the assignment card.
        // gap-4 is used to add a gap of 1 rem (16px) between the assignment cards.
        // space-y-2 is used to add a vertical space of 0.5rem (8px) between the assignment cards.
        <div className="mx-auto max-w-5xl p-8">

          <Navbar handleLogout={handleLogout} />

          <CourseList courses={courses} onCourseClick={loadAssignments}/>
          {selectedCourse && (
          // mt-8 is used to add a margin-top of 2 rem (32px) to the container. This is used to create space between the list of courses and the list of assignments.
            <AssignmentList assignments={assignments} onAssignmentClick={loadFiles} />
          )}

          {selectedAssignment && (
            <FileList files={files} />
          )}

        </div>
      )}
    </div>
  );
}

export default App;