import React, { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [parserChoice, setParserChoice] = useState("1");
  const [status, setStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleUpload = async () => {
    if (!selectedFile) {
      setStatus("Please select a file.");
      return;
    }

    setStatus("Parsing...");

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("parser", parserChoice);

    try {
      const res = await fetch("http://localhost:5001/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      if (res.ok) {
        setStatus("Parsed successfully. You can now chat.");
      } else {
        setStatus(data.error || "Error parsing file.");
      }
    } catch (err) {
      console.error(err);
      setStatus("Upload failed.");
    }
  };

  const askQuestion = async () => {
    const res = await fetch("http://localhost:5001/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div className="App">
      <h1>Zentropy PDF Chatbot</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />
      <br /><br />
      <label>Select parser:</label>
      <select value={parserChoice} onChange={(e) => setParserChoice(e.target.value)}>
        <option value="1">LlamaParse</option>
        <option value="2">Marker</option>
        <option value="3">Docling</option>
        <option value="4">Markitdown</option>
        <option value="5">Tesseract OCR</option>
        <option value="6">Hybrid (OCR + PDFPlumber)</option>
      </select>
      <br /><br />
      <button onClick={handleUpload}>Upload and Parse</button>
      <p>{status}</p>

      <hr />

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
        rows={4}
        cols={50}
      />
      <br />
      <button onClick={askQuestion}>Send</button>
      <h2>Answer:</h2>
      <p>{answer}</p>
    </div>
  );
}

export default App;