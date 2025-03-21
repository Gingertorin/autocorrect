import React, { useEffect, useState } from "react";
import WordCloud from "react-wordcloud";

const TypoWordCloud = ({ word }) => {
    const [wordCloudData, setWordCloudData] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:8000/typos/${word}`)
            .then(response => response.json())
            .then(data => {
                console.log("Fetched typo data:", data.typos);
                if (data.typos) {
                    const formattedData = data.typos.map((typo) => ({
                        text: typo.word,
                        value: typo.probability * 100, // Scale probability for better visualization
                    }));
                    formattedData.push({ text: word, value: Math.max(...formattedData.map(d => d.value)) * 1.5 }); // Ensure main word is largest
                    setWordCloudData(formattedData);
                }
            })
            .catch(error => console.error("Fetch error:", error));
    }, [word]);

    const options = {
        rotations: 2,
        rotationAngles: [0, 0], // No rotation for better readability
        fontSizes: [10, 60], // Scale word sizes
        fontFamily: "Arial",
        scale: "log",
        spiral: "archimedean",
        padding: 2,
    };

    return (
        <div style={{ width: "100%", height: "500px" }}>
            <h2 style={{ textAlign: "center" }}>Typo Word Cloud for "{word}"</h2>
            {wordCloudData.length > 0 ? (
                <WordCloud words={wordCloudData} options={options} />
            ) : (
                <p style={{ textAlign: "center" }}>Loading...</p>
            )}
        </div>
    );
};

export default TypoWordCloud;
