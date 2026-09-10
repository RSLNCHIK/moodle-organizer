import { useEffect, useState } from "react";
import CourseList from "./components/CourseList";
import Navbar from "./components/Navbar";
import LoginForm from "./components/LoginForm";
import AssignmentList from "./components/AssignmentList";
import FileList from "./components/FileList";
import NewModel from "./components/NewModel";

import { Routes, Route, Navigate, useNavigate } from "react-router-dom";

function App() {
  // Die Ansicht vor der Anmeldung: Startseite oder Loginformular.
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

  const [isLoggingIn, setIsLoggingIn] = useState(false);

  const navigate = useNavigate();
  

  async function handleLogin(event) {
    event.preventDefault();


    if (isLoggingIn) {
      return;

    }

    setError("");
    setIsLoggingIn(true);


    try {
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

      // navigate to the dashboard after successful login
      navigate("/dashboard");

    } catch {
      setError("Anmeldung konnte nicht abgeschlossen werden");
    } finally {
      setIsLoggingIn(false);
    }
    
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
    setAssignments([]);
    setFiles([]);
    setSelectedCourse(null);
    setSelectedAssignment(null);
    
    setError("");

    navigate("/login");
  }

  // ${token} comes from the state variable token, which is set when the user logs in. It is used to authenticate the request to the backend API.
  // loadAssignments takes a ${token} from the localStorage
  async function loadAssignments(courseId) {

    // setSelectedCourse is used to set the state variable selectedCourse with the courseId received from the backend API. This is used to display the assignments of the selected course in the frontend.
    setSelectedCourse(courseId);

    // setSelectedAssignment is used to set the state variable selectedAssignment to null. This is used to clear the selected assignment when a new course is selected.
    setSelectedAssignment(null);
    // setFiles is used to set the state variable files to an empty array. This is used to clear the files when a new course is selected.
    setFiles([]);
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

    // data is used to store the response from the backend API in JSON format. This is important because we need to parse the response before we can set the state variables files and selectedAssignment.
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

  // {selectedAssignment && <FileList files={files} /> } is a conditional rendering that checks if selectedAssignment is not null. If it is not null, it renders the FileList component with the files prop set to the files state variable. This is used to display the files of the selected assignment in the frontend.

  return (
    <Routes>
      {/* Startseite */}
      <Route path="/" element={<NewModel />} />

      {/* Loginformular */}
      <Route path="/login" element={
        token ? (
          <Navigate to="/dashboard" />
        ) : (
          <LoginForm 
            email={email}
            setEmail={setEmail}
            password={password}
            setPassword={setPassword}
            handleLogin={handleLogin}
            error={error}
            isLoggingIn={isLoggingIn}
            />
        )
      }
    />

    {/* Dashboard */}

    <Route path="/dashboard" element={
      token ? (
        <div className="min-h-screen bg-gray-100">
          <div className="mx-auto max-w-7xl p-8">
            <Navbar handleLogout={handleLogout} />

            <div className="grid gap-6 lg:grid-cols-3">

              <CourseList
                courses={courses}
                onCourseClick={loadAssignments}
                selectedCourse={selectedCourse}
              />

            <AssignmentList
              assignments={assignments}
              onAssignmentClick={loadFiles}
              selectedCourse={selectedCourse}
            />


            <FileList
              files={files}
              selectedAssignment={selectedAssignment}
            />

          </div>

        </div>
      </div>
    ) : (
      <Navigate to="/login" />
      )
    }
  />
  </Routes>
  );
}

export default App;
