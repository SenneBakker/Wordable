import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import AddVocabulary from './components/AddVocabulary';
import VocabularyList from './components/VocabularyList';
import PracticeMode from './components/PracticeMode';
import Statistics from './components/Statistics';

function App() {
  const [vocabulary, setVocabulary] = useState([]);
  const [currentView, setCurrentView] = useState('list');
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    fetchVocabulary();
    fetchStatistics();
  }, []);

  const fetchVocabulary = async () => {
    try {
      const response = await axios.get('/api/vocabulary');
      setVocabulary(response.data);
    } catch (error) {
      console.error('Error fetching vocabulary:', error);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await axios.get('/api/statistics');
      setStatistics(response.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  };

  const handleAddVocabulary = async (entries: Array<{id: number; word: string; translation: string; language_a: string; language_b: string }>) => {
    try {
      await axios.post('/api/vocabulary', { data: entries });
      fetchVocabulary();
      setCurrentView('list');
      
    } catch (error) {
      console.error('Error adding vocabulary:', error);
    }
  };

  const handleDeleteVocabulary = async (id: number) => {
    try {
      await axios.delete(`/api/vocabulary/${id}`);
      fetchVocabulary();
      fetchStatistics();
    } catch (error) {
      console.error('Error deleting vocabulary:', error);
    }
  };

  const handlePracticeComplete = () => {
    fetchStatistics();
    setCurrentView('list');
  };

  return (
    <div className="App">
      <header className="header">
        <h1>📚 Vocabulary Practice</h1>
        <nav className="nav">
          <button 
            className={`nav-btn ${currentView === 'list' ? 'active' : ''}`}
            onClick={() => setCurrentView('list')}
          >
            Words List
          </button>
          <button 
            className={`nav-btn ${currentView === 'add' ? 'active' : ''}`}
            onClick={() => setCurrentView('add')}
          >
            Add Word
          </button>
          <button 
            className={`nav-btn ${currentView === 'practice' ? 'active' : ''}`}
            onClick={() => setCurrentView('practice')}
            disabled={vocabulary.length === 0}
          >
            Practice
          </button>
          <button 
            className={`nav-btn ${currentView === 'stats' ? 'active' : ''}`}
            onClick={() => setCurrentView('stats')}
          >
            Statistics
          </button>
        </nav>
      </header>

      <main className="main-content">
        {currentView === 'list' && (
          <VocabularyList 
            vocabulary={vocabulary}
            onDelete={handleDeleteVocabulary}
          />
        )}
        {currentView === 'add' && (
          <AddVocabulary onAdd={handleAddVocabulary} />
        )}
        {currentView === 'practice' && vocabulary.length > 0 && (
          <PracticeMode 
            vocabulary={vocabulary}
            onComplete={handlePracticeComplete}
          />
        )}
        {currentView === 'stats' && statistics && (
          <Statistics statistics={statistics} />
        )}
      </main>
    </div>
  );
}

export default App;
