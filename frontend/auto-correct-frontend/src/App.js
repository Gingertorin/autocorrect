import React, { useState } from "react";
import axios from "axios";

function App() {
    const [text, setText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [language, setLanguage] = useState("");

    const handleDetectLanguage = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/detect_language", { text });
            setLanguage(response.data.detected_language);
        } catch (error) {
            console.error("Error detecting language:", error);
        }
    };

    const handleCorrectText = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/correct_word", { text });
            setCorrectedText(response.data.corrected_text);
        } catch (error) {
            console.error("Error correcting text:", error);
        }
    };

    return (
        <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
            <h1>Multilingual Autocorrect</h1>
            <textarea
                rows="4"
                cols="50"
                placeholder="Type here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
            />
            <div>
                <button onClick={handleDetectLanguage} style={{ margin: "5px" }}>Detect Language</button>
                <button onClick={handleCorrectText} style={{ margin: "5px" }}>Correct Text</button>
            </div>
            {language && <h2>Detected Language: {language}</h2>}
            {correctedText && <h2>Corrected Text: {correctedText}</h2>}
        </div>
    );
}

export default App;
