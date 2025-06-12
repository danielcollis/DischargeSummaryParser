import React, { useState } from 'react';

function App() {
  const [summary, setSummary] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    const res = await fetch('/api/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ summary }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  }

  return (
    <div style={{ margin: '2rem' }}>
      <h1>Discharge Summary Parser</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="6"
          cols="60"
          value={summary}
          onChange={e => setSummary(e.target.value)}
          placeholder="Paste discharge summary here..."
        />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? 'Parsing...' : 'Parse'}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: '1rem' }}>
          <h2>Parsed Results:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;