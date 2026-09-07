import { useEffect, useState } from "react";
import CourseList from "./components/CourseList";
import Navbar from "./components/Navbar";
import LoginForm from "./components/LoginForm";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");

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
        <div className="mx-auto max-w-5xl p-8">

          <Navbar handleLogout={handleLogout} />

          <CourseList courses={courses} />

        </div>
      )}
    </div>
  );
}

export default App;