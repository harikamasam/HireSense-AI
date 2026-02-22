import React, { useState } from "react";
import axios from "axios";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

function App() {
  const [resumeText, setResumeText] = useState("");
  const [job, setJob] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!job) {
      alert("Please enter Job Description");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("job_description", job);

    if (file) {
      formData.append("resume_file", file);
    } else if (resumeText) {
      formData.append("resume_text", resumeText);
    } else {
      alert("Please upload resume or paste resume text");
      setLoading(false);
      return;
    }

    try {
      const res = await axios.post(
        "http://localhost:8000/analyze",
        formData
      );
      setResult(res.data);
    } catch (err) {
      alert("Backend not connected or error occurred");
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(to right, #141e30, #243b55)",
        padding: "40px",
        color: "white",
        fontFamily: "Segoe UI",
      }}
    >
      <h1 style={{ textAlign: "center", fontSize: "42px" }}>
        HireSense AI 🚀
      </h1>

      <div style={{ marginTop: "30px" }}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      <textarea
        placeholder="Or Paste Resume Text"
        rows="6"
        value={resumeText}
        onChange={(e) => setResumeText(e.target.value)}
        style={{
          width: "100%",
          marginTop: "15px",
          padding: "10px",
          borderRadius: "10px",
        }}
      />

      <textarea
        placeholder="Paste Job Description"
        rows="6"
        value={job}
        onChange={(e) => setJob(e.target.value)}
        style={{
          width: "100%",
          marginTop: "15px",
          padding: "10px",
          borderRadius: "10px",
        }}
      />

      <button
        onClick={analyze}
        style={{
          marginTop: "20px",
          padding: "12px 30px",
          borderRadius: "25px",
          border: "none",
          background: "#ff9800",
          fontSize: "18px",
          cursor: "pointer",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {result && (
        <div
          style={{
            background: "white",
            color: "black",
            marginTop: "30px",
            padding: "20px",
            borderRadius: "15px",
          }}
        >
          <div style={{ width: "150px", margin: "20px auto" }}>
            <CircularProgressbar
              value={result.match_score}
              text={`${result.match_score}%`}
              styles={buildStyles({
                textSize: "16px",
                pathColor:
                  result.match_score > 75
                    ? "green"
                    : result.match_score >= 50
                    ? "orange"
                    : "red",
                textColor: "#000",
              })}
            />
          </div>

          <h3 style={{ textAlign: "center" }}>
            {result.match_strength}
          </h3>

          <h4>Category Scores</h4>
          <p>Technical: {result.tech_score}%</p>
          <p>Tools: {result.tools_score}%</p>
          <p>Soft Skills: {result.soft_score}%</p>

          <h4>Missing Keywords</h4>
          <ul>
            {result.missing_keywords?.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>

          <h4>Missing Resume Sections</h4>
          <ul>
            {result.missing_sections?.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>

          <p>
            <strong>Suggestion:</strong> {result.suggestion}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;