import { useState } from "react";

import { useNavigate } from "react-router-dom";

import InteractiveGridBackground from "./InteractiveGridBackground";

function RegisterForm() {
    const navigate = useNavigate();


    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordRepeat, setPasswordRepeat] = useState("");

    const [error, setError] = useState("");
    const [isRegistering, setIsRegistering] = useState(false);

    async function handleRegister(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        setError("");

        if (password !== passwordRepeat) {
            setError("Passwoerter stimmen nicht ueberein");
            return;

        }

        setIsRegistering(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/register", 
                {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: email,
                    password: password,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                setError(data.detail || "Registrierung fehlgeschlagen");
                return;
            }

            navigate("/login");

        } catch (error) {
            setError("Backend konnte nicht erreicht werden");
        } finally {

            setIsRegistering(false);
        }

    }

    return (
        <div className="relative min-h-screen overflow-hidden bg-slate-50">
            <InteractiveGridBackground />

            {/* // absolute is used to position the div element relative to its nearest positioned ancestor.
            // left-1/4 is used to position the div element 25% from the left edge of its containing container.
            // top-1/3 is used to position the div element 33.33% from the top edge of its containing container.
            // h-72 is used to set the height of the div element to 18rem
            // w-72 is used to set the width of the div element to 18rem
            // rounded-full is used to make the div element a perfect circle by setting its border radius to 50%.
            // bg-violet-200/40 is used to set the background color of the div element to a semi-transparent violet color with 40% opacity.
            // blur-3xl is used to apply a blur effect to the div element, making it appear soft and out of focus. 
            // */}

            <div className="pointer-events-none absolute left-1/4 top-1/3 h-72 w-72 rounded-full bg-violet-200/40 blur-3xl"/>

            
            
            <div className="pointer-events-none absolute bottom-1/4 right-1/4 h-72 w-72 rounded-full bg-blue-200/40 blur-3xl"/>
        
            <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-4">
                <div className="w-full max-w-sm">
                    <div className="mb-6 text-center">
                        <span className="text-2xl font-bold text-blue-600">
                            Moodle Organizer - Registrierung
                        </span>
                    </div>
                </div>

                <form 
                onSubmit={handleSubmit}
                className="rounded-2xl bg-white p-7 shadow-xl shadow-gray-200/70">
                    <button
                    type="submit"
                    onClick={() => navigate("/login")} 
                    className="mb-5 cursor-pointer text-sm font-medium text-gray-500 transition hover:text-gray-900">
                    ← Zurück zum Login
                    </button>

                    <div className="mb-7 text-center">
                        <h1 className="text-2xl font-bold text-gray-900">Registrierung</h1>

                        <p className="mt-2 text-sm text-gray-500">
                            Registriere dich für Moodle Organizer.
                        </p>
                    </div>

                    <div className="mb-4">
                        <label className="mb-2 block text-sm font-medium text-gray-800">
                            E-Mail
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            placeholder="E-Mail"
                            className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 fokus:ring-blue-100"/>
                    </div>


                    <div className="mb-6">
                        <label className="mb-2 block text-sm font-medium text-gray-800">
                            Passwort
                        </label>


                        <input
                            type="password"
                            value={passwordRepeat}
                            onChange={(event) => setPasswordRepeat(event.target.value)}
                            placeholder="••••••••"
                            className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                        />

                    </div>

                    {error && (
                        <p className="mb-4 text-sm text-red-500">{error}</p>
                    )}

                    <button className="w-full cursor-pointer rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 diabled:cursor-not-allowed  disabled:opacity-60">
                        {isRegistering ? "Registrierung..." : "Konto erstellen"}
                    </button>
                </form>
            </div>
        </div>
    )

}

export default RegisterForm;