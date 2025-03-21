import React, { useState } from "react";

const App = () => {
    const [word, setWord] = useState("hello");
    const [imageUrl, setImageUrl] = useState("");

    const fetchWordCloud = () => {
        setImageUrl(`http://localhost:8000/wordcloud/${word}`);
    };

    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h1>Word Cloud for Typo Visualization</h1>
            <input
                type="text"
                value={word}
                onChange={(e) => setWord(e.target.value)}
                placeholder="Enter a word"
                style={{ padding: "10px", fontSize: "16px", marginBottom: "10px" }}
            />
            <button onClick={fetchWordCloud} style={{ padding: "10px 20px", fontSize: "16px" }}>
                Generate Word Cloud
            </button>
            <br />
            {imageUrl && <img src={imageUrl} alt="Word Cloud" style={{ marginTop: "20px", width: "80%" }} />}
        </div>
    );
};

export default App;
