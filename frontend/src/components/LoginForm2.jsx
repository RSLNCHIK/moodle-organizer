function LoginForm2({
    email,
    setEmail,
    password,
    setPassword,
    handleLogin,
    error,
    onBack
}) {
    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
          <form
            onSubmit={handleLogin}
            className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg"
          >
            <button
              type="button"
              onClick={onBack}
              className="mb-4 cursor-pointer text-sm text-gray-600 hover:text-violet-700 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-violet-600"
            >
              Zur Startseite
            </button>
            <h1 className="mb-6 text-3xl font-bold">
              Moodle Organizer
            </h1>

            <div className="mb-4">
              <label className="mb-1 block font-medium">
                E-Mail
              </label>

              <input
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                className="w-full rounded-lg border border-gray-300 px-4 py-2"
              />
            </div>

            <div className="mb-4">
              <label className="mb-1 block font-medium">
                Passwort
              </label>

              <input
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                className="w-full rounded-lg border border-gray-300 px-4 py-2"
              />
            </div>

            {error && (
              <p className="mb-4 text-red-600">
                {error}
              </p>
            )}

            <button
              type="submit"
              className="w-full rounded-lg bg-black px-4 py-2 font-medium text-white hover:bg-gray-800"
            >
              Einloggen
            </button>
          </form>
        </div>
    )
}

export default LoginForm2
