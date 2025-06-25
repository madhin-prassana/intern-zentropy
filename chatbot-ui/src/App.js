import React, { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

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
      <h1>Chat with PDF</h1>
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