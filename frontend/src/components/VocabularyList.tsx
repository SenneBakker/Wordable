import React from 'react';

function VocabularyList({ vocabulary, onDelete }) {
  return (
    <div className="vocabulary-list">
      <h2>Your Vocabulary ({vocabulary.length})</h2>
      {vocabulary.length === 0 ? (
        <p className="empty-message">No vocabulary yet. Add some words to get started!</p>
      ) : (
        <div className="vocab-table">
          <table>
            <thead>
              <tr>
                <th>Word</th>
                <th>Translation</th>
                <th>Language</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {vocabulary.map((item) => (
                <tr key={item.id}>
                  <td>{item.word}</td>
                  <td>{item.translation}</td>
                  <td>{item.language}</td>
                  <td>
                    <button 
                      className="btn btn-danger"
                      onClick={() => onDelete(item.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default VocabularyList;
