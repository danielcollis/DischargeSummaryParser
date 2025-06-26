import React, { useState } from 'react';

function App() {
  const [summary, setSummary] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);
  
    try {
      const res = await fetch('/api/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ summary }),
      });
  
      if (!res.ok) throw new Error((await res.json()).detail);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
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
          <button onClick={() => {
  navigator.clipboard.writeText(JSON.stringify(result, null, 2));
}}>
  Copy to Clipboard
</button>

<button onClick={() => {
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'parsed_summary.json';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}}>
  Download JSON
</button>
        </div>
      )}
      {error && <div style={{ color: "red" }}>{error}</div>}
    </div>
  );
}

export default App;