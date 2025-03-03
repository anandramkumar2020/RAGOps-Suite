import { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')
  const [contexts, setContexts] = useState([])
  const [loading, setLoading] = useState(false)
  const [showJson, setShowJson] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch(`http://localhost:8000/api/query?query_text=${encodeURIComponent(query)}`)
      const data = await res.json()
      setResponse(data.response)
      setContexts(data.contexts || [])
    } catch (error) {
      console.error('Error:', error)
      setResponse('Error occurred while fetching response')
    }
    setLoading(false)
  }

  return (
    <div className="container">
      <h1>RAG Query Interface</h1>
      <form onSubmit={handleSubmit} className="query-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query..."
          className="query-input"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Submit'}
        </button>
      </form>
      {response && (
        <div className="response-container">
          <div className="response">
            <h2>Response:</h2>
            <p>{response}</p>
          </div>
          {contexts.length > 0 && (
            <div className="sources-section">
              <div className="sources-header">
                <h3>Sources</h3>
                <button 
                  className="toggle-json" 
                  onClick={() => setShowJson(!showJson)}
                >
                  {showJson ? 'Show Summary' : 'Show JSON'}
                </button>
              </div>
              {showJson ? (
                <pre className="json-view">
                  <code>
                    {JSON.stringify(contexts, null, 2)}
                  </code>
                </pre>
              ) : (
                <div className="sources-grid">
                  {contexts.map((ctx, index) => (
                    <div key={index} className="source-item">
                      <div className="source-header">
                        <strong>{ctx.metadata.file_name}</strong>
                        <span className="score">({(ctx.score * 100).toFixed(1)}% relevant)</span>
                      </div>
                      <div className="metadata-info">
                        <span>Type: {ctx.metadata.file_type?.split('/').pop()}</span>
                        <span>Size: {(ctx.metadata.file_size / 1024).toFixed(1)} KB</span>
                        <span>Modified: {new Date(ctx.metadata.last_modified_date).toLocaleDateString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
