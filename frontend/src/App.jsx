import React, { useState } from 'react';

// Add dark theme styles
const appStyles = `
  body {
    background: #181a1b;
    color: #f5f6fa;
    font-family: Consolas, monospace;
    margin: 0;
    min-height: 100vh;
  }
  .center-container {
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #181a1b;
  }
  .card {
    background: #23272f;
    border-radius: 18px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    padding: 2.5rem 2.5rem 2rem 2.5rem;
    max-width: 600px;
    width: 100%;
    min-width: 350px;
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  h1, h2 {
    color: #4da3ff;
    font-family: Consolas, monospace;
    text-align: center;
  }
  textarea {
    width: 100%;
    max-width: 500px;
    min-width: 200px;
    background: #181a1b;
    color: #f5f6fa;
    border: 1.5px solid #4da3ff;
    border-radius: 10px;
    padding: 1rem;
    font-size: 1rem;
    font-family: Consolas, monospace;
    margin-bottom: 1rem;
    resize: vertical;
    transition: border 0.2s;
  }
  textarea:focus {
    outline: none;
    border-color: #82cfff;
  }
  .button-row {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }
  button {
    font-family: Consolas, monospace;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
    margin-top: 0.5rem;
  }
  .primary-btn {
    background: #4da3ff;
    color: #181a1b;
    font-weight: bold;
  }
  .primary-btn:hover {
    background: #82cfff;
  }
  .secondary-btn {
    background: #23272f;
    color: #f5f6fa;
    border: 1.5px solid #4da3ff;
  }
  .secondary-btn:hover {
    background: #31363f;
  }
  pre {
    background: #181a1b;
    color: #f5f6fa;
    border-radius: 10px;
    padding: 1rem;
    font-size: 1rem;
    font-family: Consolas, monospace;
    border: 1.5px solid #31363f;
    overflow-x: auto;
    margin-top: 0.5rem;
  }
  .error {
    color: #ff4d6d;
    margin-top: 1rem;
    text-align: center;
  }
`;

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
    <>
      <style>{appStyles}</style>
      <div style={{ color: '#b0b3b8', textAlign: 'center', fontSize: '1.35rem', fontWeight: 600, width: '100vw', marginBottom: '2.5rem', marginTop: '1.5rem', letterSpacing: 0.2 }}>
        AI-Driven Discharge Summary Parser – Automating Medical<br />
        Entity Extraction and Standardization Using NLP
      </div>
      <nav style={{ width: '100vw', display: 'flex', justifyContent: 'center', alignItems: 'center', background: '#23272f', padding: '0.75rem 0', marginBottom: '0.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.15)' }}>
        <a href="https://spacy.io/" style={{ color: '#82cfff', textDecoration: 'none', margin: '0 1.5rem', fontWeight: 500, fontSize: '1.05rem' }}>spaCy</a>
        <a href="https://allenai.github.io/scispacy/" style={{ color: '#82cfff', textDecoration: 'none', margin: '0 1.5rem', fontWeight: 500, fontSize: '1.05rem' }}>SciSpaCy</a>
        <a href="https://github.com/danielcollis/senior-project" style={{ color: '#82cfff', textDecoration: 'none', margin: '0 1.5rem', fontWeight: 500, fontSize: '1.05rem' }}>GitHub</a>
      </nav>
      <div className="center-container" style={{ marginTop: 0 }}>
        <div className="card" style={{ marginTop: '2.5rem' }}>
          <h1>Discharge Summary Parser</h1>
          <form onSubmit={handleSubmit}>
            <textarea
              rows="6"
              value={summary}
              onChange={e => setSummary(e.target.value)}
              placeholder="Paste discharge summary here..."
            />
            <div className="button-row">
              <button className="primary-btn" type="submit" disabled={loading}>
                {loading ? 'Parsing...' : 'Parse'}
              </button>
            </div>
          </form>

          {result && (
            <div style={{ marginTop: '1.5rem' }}>
              <h2>Parsed Results:</h2>
              <pre>{JSON.stringify(result, null, 2)}</pre>
              <div className="button-row">
                <button className="secondary-btn" onClick={() => {
                  navigator.clipboard.writeText(JSON.stringify(result, null, 2));
                }}>
                  Copy to Clipboard
                </button>
                <button className="secondary-btn" onClick={() => {
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
            </div>
          )}
          {error && <div className="error">{error}</div>}
        </div>
      </div>
    </>
  );
}

export default App;