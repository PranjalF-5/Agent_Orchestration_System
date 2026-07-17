import { useState } from 'react'
import './App.css'

interface TaskResponse {
  task_id: string;
  status: string;
  result: string | null;
  plan: string | null;
}

function App() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<TaskResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      // Send request to our FastAPI backend
      const res = await fetch('http://127.0.0.1:8000/tasks/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prompt: prompt,
          tenant_id: 'frontend_user',
          config: {}
        })
      })

      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`)
      }

      const data: TaskResponse = await res.json()
      setResponse(data)
    } catch (err: any) {
      setError(err.message || 'Failed to communicate with the Agent')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>Agent Orchestration</h1>
        <p>Give the AI an objective, and watch it plan and execute.</p>
      </header>

      <main>
        <div className="glass-panel">
          <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <input
              type="text"
              className="input-field"
              placeholder="e.g. Calculate 45 * 123 + 999 or Search for AI news in 2026..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={loading}
            />
            <button type="submit" className="btn-primary" disabled={loading || !prompt.trim()}>
              {loading ? 'Processing...' : 'Run Agent'}
            </button>
          </form>
        </div>

        {loading && (
          <div className="glass-panel result-section animate-pulse" style={{ textAlign: 'center' }}>
            <h3 style={{ margin: 0, color: 'var(--accent-primary)' }}>Agent is thinking...</h3>
            <p style={{ marginTop: '8px', color: 'var(--text-secondary)' }}>
              The Supervisor, Planner, and Executor are working on your task. This may take 15-30 seconds.
            </p>
          </div>
        )}

        {error && (
          <div className="glass-panel result-section" style={{ borderColor: 'rgba(239, 68, 68, 0.4)' }}>
            <h3 style={{ color: '#ef4444' }}>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {response && !loading && (
          <div className="result-section">
            <div className="glass-panel">
              <h2 style={{ color: 'var(--accent-primary)' }}>Task Completed</h2>
              <p style={{ color: 'var(--text-secondary)', marginBottom: '16px' }}>
                Task ID: {response.task_id}
              </p>
              
              {response.plan && (
                <div style={{ marginBottom: '24px' }}>
                  <h3>Agent Plan</h3>
                  <div className="plan-content">{response.plan}</div>
                </div>
              )}

              <div>
                <h3>Final Result</h3>
                <div className="result-content" style={{ borderColor: 'var(--accent-primary)' }}>
                  {response.result || "No result returned"}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
