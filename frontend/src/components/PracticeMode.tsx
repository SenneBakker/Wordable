import React, { useState } from 'react';
import axios from 'axios';

function PracticeMode({ vocabulary, onComplete }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showTranslation, setShowTranslation] = useState(false);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(0);

  const current = vocabulary[currentIndex];

  const handleCorrect = async () => {
    try {
      await axios.post('/api/practice', {
        vocabulary_id: current.id,
        is_correct: 1
      });
      setScore(score + 1);
      next();
    } catch (error) {
      console.error('Error recording practice:', error);
    }
  };

  const handleIncorrect = async () => {
    try {
      await axios.post('/api/practice', {
        vocabulary_id: current.id,
        is_correct: 0
      });
      next();
    } catch (error) {
      console.error('Error recording practice:', error);
    }
  };

  const next = () => {
    const newAnswered = answered + 1;
    setAnswered(newAnswered);

    if (newAnswered < vocabulary.length) {
      setCurrentIndex(currentIndex + 1);
      setShowTranslation(false);
    } else {
      onComplete();
    }
  };

  return (
    <div className="practice-mode">
      <div className="practice-progress">
        <p>Progress: {answered} / {vocabulary.length}</p>
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${(answered / vocabulary.length) * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="practice-card">
        <h2>{current.word}</h2>
        <p className="language-tag">{current.language}</p>

        {showTranslation && (
          <div className="translation">
            <p className="translation-text">{current.translation}</p>
          </div>
        )}

        <button 
          className="btn btn-secondary"
          onClick={() => setShowTranslation(!showTranslation)}
        >
          {showTranslation ? 'Hide' : 'Show'} Translation
        </button>

        <div className="practice-actions">
          <button 
            className="btn btn-danger"
            onClick={handleIncorrect}
          >
            ✗ Incorrect
          </button>
          <button 
            className="btn btn-success"
            onClick={handleCorrect}
          >
            ✓ Correct
          </button>
        </div>

        <div className="practice-stats">
          <p>Current Score: <strong>{score} / {answered}</strong></p>
          {answered > 0 && (
            <p>Accuracy: <strong>{((score / answered) * 100).toFixed(1)}%</strong></p>
          )}
        </div>
      </div>
    </div>
  );
}

export default PracticeMode;
