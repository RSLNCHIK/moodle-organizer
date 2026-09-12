import InteractiveGridBackground from "./InteractiveGridBackground";
import { useNavigate } from "react-router-dom";

function LoginForm({
  email,
  setEmail,
  password,
  setPassword,
  handleLogin,
  error,
  isLoggingIn
}) {

  const navigate = useNavigate();
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-50">
      <InteractiveGridBackground />

      {/* weiche Farbflächen im Hintergrund */}
      <div className="pointer-events-none absolute left-1/4 top-1/3 h-72 w-72 rounded-full bg-violet-200/40 blur-3xl" />

      <div className="pointer-events-none absolute bottom-1/4 right-1/4 h-72 w-72 rounded-full bg-blue-200/40 blur-3xl" />

      {/* Inhalt */}
      // relative is used to position the div element relative to its normal position in the document flow.
      // z-10 is used to set the z-index of the div element to 10, which determines its stacking order relative to other elements on the page. A higher z-index value means the element will be displayed in front of elements with lower z-index values.
      <div className="relative z-10 flex min-h-screen items-center justify-center px-4">
        <div className="w-full max-w-sm">
          <div className="mb-6 flex items-center justify-center">
            <span className="text-2xl font-bold text-blue-600">
              Moodle Organizer
            </span>
          </div>

          {/* Login Card */}
          <form
            onSubmit={handleLogin}
            className="rounded-2xl bg-white p-7 shadow-xl shadow-gray-200/70"
          >
            <button
              type="button"
              onClick={() => navigate("/")}
              className="mb-5 cursor-pointer text-sm font-medium text-gray-500 transition hover:text-gray-900"
            >
              ← Zur Startseite
            </button>

            <div className="mb-7 text-center">
              <h1 className="text-2xl font-bold text-gray-900">
                Welcome back
              </h1>

              <p className="mt-2 text-sm text-gray-500">
                Sign in to continue to your courses.
              </p>
            </div>

            {/* E-Mail */}
            <div className="mb-5">
              <label htmlFor="email" className="mb-2 block text-sm font-semibold text-gray-800">
                E-Mail
              </label>

              <input
                id="email"
                required
                autoComplete="username"
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                placeholder="you@example.com"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              />
            </div>

            {/* Passwort */}
            <div className="mb-6">
              <label htmlFor="password" className="mb-2 block text-sm font-semibold text-gray-800">
                Passwort
              </label>

              <input
                id="password"
                required
                autoComplete="current-password"
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                placeholder="••••••••"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              />
            </div>

            {error && (
              <p className="mb-4 text-sm text-red-600">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={isLoggingIn}
              className="w-full cursor-pointer rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:opacity-60 disabled:cursor-wait disabled:hover:bg-blue-600"
            >
              {isLoggingIn ? "Logging in..." : "Continue"}
            </button>


            {/* // Register Link, if the user does not have an account, they can navigate to the register page */}
              <p className="relative top-3 text-center text-sm text-gray-500">
                Noch kein Konto?{" "}
                <button
                  type="button"
                  onClick={() => navigate("/register")}
                  className="cursor-pointer text-sm font-medium text-blue-600 transition hover:text-blue-800"
                >
                  Konto erstellen
                </button>
              </p>

          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginForm;
