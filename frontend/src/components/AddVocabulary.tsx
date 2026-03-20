import React from 'react';
import TextField from '@mui/material/TextField';


function AddVocabulary({ onAdd }) {
  const [language_a, setLanguage_a] = React.useState('English');
  const [language_b, setLanguage_b] = React.useState('Portuguese');
  const [entries, setEntries] = React.useState([{ id: 0, word: '', translation: '' }]);
  const [nextId, setNextId] = React.useState(1);

  const handleWordChange = (id: number, value: string) => {
    setEntries(entries.map(entry => 
      entry.id === id ? { ...entry, word: value } : entry
    ));
  };

  const handleTranslationChange = (id: number, value: string) => {
    setEntries(entries.map(entry => 
      entry.id === id ? { ...entry, translation: value } : entry
    ));
  };

  const handleAddRow = () => {
    setEntries([...entries, { id: nextId, word: '', translation: '' }]);
    setNextId(nextId + 1);
  };

  const handleRemoveRow = (id: number) => {
    if (entries.length > 1) {
      setEntries(entries.filter(entry => entry.id !== id));
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const validEntries = entries.filter(entry => entry.word.trim() && entry.translation.trim());
  

    if (validEntries.length > 0) {
      onAdd(entries);
      setEntries([{ id: nextId, word: '', translation: '' }]);
      setNextId(nextId + 1);
    }
  };

  return (
    <div className="add-vocabulary">
      <h2>Add new wordlist</h2>
      <form onSubmit={handleSubmit} className="form">
          <h3>Name of new list</h3>
          <div>
            <input
                type="text"
                placeholder="Name of list"
                className="entry-input"
                id="NameOfNewWorlist"
                />
          </div>
        {/* Language Selection Section */}
        <div className="language-selection">
          <div className="form-group">
            <label htmlFor="language_a">Language 1:</label>
            <select 
              id="language_a"
              value={language_a}
              onChange={(e) => setLanguage_a(e.target.value)}
            >
              <option>English</option>
              <option>French</option>
              <option>Polish</option>
              <option>Italian</option>
              <option>Portuguese</option> 
              <option>Dutch</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="language_b">Language 2:</label>
            <select 
              id="language_b"
              value={language_b}
              onChange={(e) => setLanguage_b(e.target.value)}
            >
              <option>English</option>
              <option>French</option>
              <option>Polish</option>
              <option>Italian</option>
              <option>Portuguese</option> 
              <option>Dutch</option>
            </select>
          </div>
        </div>

        {/* Input Rows Section */}
        <div className="vocabulary-entries">
          <div className="entries-header">
            <div className="entry-column">{language_a}</div>
            <div className="entry-column">{language_b}</div>
          </div>
          
          {entries.map((entry) => (
            <div key={entry.id} className="entry-row">
              <input
                type="text"
                value={entry.word}
                onChange={(e) => handleWordChange(entry.id, e.target.value)}
                placeholder={`Enter ${language_a.toLowerCase()}`}
                className="entry-input"
              />
              <input
                type="text"
                value={entry.translation}
                onChange={(e) => handleTranslationChange(entry.id, e.target.value)}
                placeholder={`Enter ${language_b.toLowerCase()}`}
                className="entry-input"
              />
              {entries.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleRemoveRow(entry.id)}
                  className="btn btn-remove"
                >
                  X
                </button>
              )}
            </div>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="form-actions">
          <button type="button" onClick={handleAddRow} className="btn btn-secondary">
            + Add Row
          </button>
          <button type="submit" className="btn btn-primary">
            Save All
          </button>
        </div>
      </form>
    </div>
  );
}

export default AddVocabulary;
