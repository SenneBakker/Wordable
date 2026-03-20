import React from 'react';

function Statistics({ statistics }) {
  return (
    <div className="statistics">
      <h2>Your Statistics</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Words</h3>
          <p className="stat-value">{statistics.total_words}</p>
        </div>
        <div className="stat-card">
          <h3>Total Attempts</h3>
          <p className="stat-value">{statistics.total_attempts}</p>
        </div>
        <div className="stat-card">
          <h3>Correct Answers</h3>
          <p className="stat-value">{statistics.correct_attempts}</p>
        </div>
        <div className="stat-card">
          <h3>Accuracy Rate</h3>
          <p className="stat-value">{statistics.accuracy}%</p>
        </div>
      </div>
    </div>
  );
}

export default Statistics;
