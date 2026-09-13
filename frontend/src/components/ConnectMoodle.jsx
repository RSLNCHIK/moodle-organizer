import { useState } from "react";
import { useNavigate } from "react-router-dom";

import InteractiveGridBackground from "./InteractiveGridBackground";


function ConnectMoodle({ accessToken }) {
    const navigate = useNavigate();

    const [baseUrl, setBaseUrl] = useState("https://moodle2.uni-potsdam.de/webservice/rest/server.php");
    const [moodleToken, setMoodleToken] = useState("");

    const [error, setError] = useState("");

    const [isConnecting, setIsConnecting] = useState(false);

    async function handleConnect(event) {
        // Prevent the default form submission behavior
        // This is important to avoid the page from reloading when the form is submitted.
        // It allows us to handle the form submission with our own logic.
        event.preventDefault();

        setError("");

        setIsConnecting(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/moodle-connection",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${accessToken}`,
                    },
                    body: JSON.stringify({
                        base_url: baseUrl,
                        token: moodleToken,
                    })
                }
            );
            const data = await response.json();

            // Log the response status and data for debugging purposes
            console.log("Status:", response.status);
            console.log("Antwort:", data);

            if (!response.ok) {
                setError(data.detail || "Verbindung zu Moodle fehlgeschlagen");
                return;
            }

            // Navigate to the dashboard after successfull connection
            navigate("/dashboard");
        
        } catch (error) {
            setError("Backend konnte nicht erreicht werden");
        } finally {
            setIsConnecting(false);
        }


    }

    return (
        <div className="relative min-h-screen overflow-hidden bg-slate-50">
            <InteractiveGridBackground />

            <div className="relative z-10 flex min-h-screen items-center justify-center">
                <form onSubmit={handleConnect} className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
                    <div className="mb-7 text-center">
                        <h1 className="text-2xl font-bold">Moodle verbinden</h1>

                        <p className="mt-2 text-sm text-gray-500">Verbinden Sie Ihr Moodle-Konto mit unserem System.</p>

                    </div>

                    <div className="mb-5">
                        <label className="mb-2 block text-sm font-semibold">
                            Moodle-URL
                        </label>

                        <input type="text" value={baseUrl} onChange={(event) => setBaseUrl(event.target.value)} placeholder="Moodle Webservice Token" className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500" />

                    </div>

                    <div className="mb-5">
                        <label className="mb-2 block text-sm font-semibold">
                            Moodle-Token
                        </label>

                        <input
                            type="password"
                            value={moodleToken}
                            onChange={(event) => setMoodleToken(event.target.value)}
                            placeholder="Moodle Webservice Token"
                            required
                            className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500"
                        />
                    </div>

                    {error && (
                        <p className="mb-5 text-sm text-red-600">
                            {error}
                        </p>
                    )}

                    <button type="submit" disabled={isConnecting} className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:opacity-60">
                        {isConnecting ? "Verbinden..." : "Moodle verbinden"}
                    </button>
                </form>

            </div>
        </div>
    )

}

export default ConnectMoodle;