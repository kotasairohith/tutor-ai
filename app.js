import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [questionType, setQuestionType] = useState("multiple-choice");
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/generate-question", {
        topic,
        difficulty,
        question_type: questionType,
      });
      setQuestion(response.data);
    } catch (error) {
      console.error("Error generating question:", error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Personalized Learning Platform</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter a topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          required
        />
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
        <select value={questionType} onChange={(e) => setQuestionType(e.target.value)}>
          <option value="multiple-choice">Multiple Choice</option>
          <option value="short-answer">Short Answer</option>
          <option value="true-false">True/False</option>
        </select>
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Question"}
        </button>
      </form>
      {question && (
        <div>
          <h2>Generated Question</h2>
          <p>{question.question}</p>
          {question.options.length > 0 && (
            <ul>
              {question.options.map((option, index) => (
                <li key={index}>{option}</li>
              ))}
            </ul>
          )}
          <p><strong>Answer:</strong> {question.answer}</p>
        </div>
      )}
    </div>
  );
};

export default App;
