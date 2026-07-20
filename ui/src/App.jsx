import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { Toaster, toast } from 'react-hot-toast'
import { Terminal, Database, Play, FileJson, X, RefreshCw } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import './index.css'

function App() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [plan, setPlan] = useState(null)
  const [executionLogs, setExecutionLogs] = useState([])
  const [executing, setExecuting] = useState(false)
  const wsRef = useRef(null)
  const logsEndRef = useRef(null)

  useEffect(() => {
    // Auto-scroll logs
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [executionLogs])

  const handleParse = async () => {
    if (!prompt.trim()) return
    setLoading(true)
    try {
      const res = await axios.post('http://localhost:8080/parse-intent', { prompt })
      setPlan(res.data.plan)
      toast.success('Generated execution plan')
    } catch (err) {
      toast.error('Failed to parse intent. Is the backend running?')
    }
    setLoading(false)
  }

  const handleRemoveTable = (table) => {
    setPlan(plan.filter(t => t !== table))
  }

  const handleExecute = async () => {
    if (!plan || plan.length === 0) return
    setExecuting(true)
    setExecutionLogs(["Connecting to backend..."])
    
    // Connect to WebSocket
    wsRef.current = new WebSocket('ws://localhost:8080/ws/logs')
    wsRef.current.onmessage = (event) => {
      setExecutionLogs(prev => [...prev, event.data])
      if (event.data.includes("Pipeline finished")) {
        setExecuting(false)
        wsRef.current.close()
      }
    }

    try {
      await axios.post('http://localhost:8080/execute', { tables: plan, rows: 50 })
      toast.success('Execution started')
    } catch (err) {
      toast.error('Failed to start execution')
      setExecuting(false)
      if (wsRef.current) wsRef.current.close()
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans selection:bg-indigo-500/30">
      <Toaster position="top-right" toastOptions={{ style: { background: '#1e293b', color: '#fff' } }} />
      
      <header className="mb-10 flex items-center justify-between border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/20 rounded-lg">
            <Database className="text-indigo-400 w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">ETS Sandbox</h1>
            <p className="text-slate-500 text-sm">Smart Test Data Generator</p>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Left Column: Input and Execution */}
        <div className="space-y-6">
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl backdrop-blur-xl">
            <h2 className="text-lg font-medium mb-4 flex items-center gap-2">
              <Terminal className="w-5 h-5 text-indigo-400" />
              Natural Language Prompt
            </h2>
            <textarea 
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g., Generate 50 records for provider addresses and taxonomy..."
              className="w-full h-32 bg-slate-950 border border-slate-800 rounded-lg p-4 text-slate-300 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none mb-4"
            />
            <button 
              onClick={handleParse}
              disabled={loading || executing}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : 'Compile Plan'}
            </button>
          </section>

          {/* Logs */}
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl h-80 flex flex-col">
             <h2 className="text-lg font-medium mb-4 flex items-center gap-2 text-slate-400">
               <FileJson className="w-5 h-5" /> Execution Logs
             </h2>
             <div className="flex-1 bg-slate-950 rounded-lg border border-slate-800 p-4 font-mono text-sm overflow-y-auto text-green-400/80">
               {executionLogs.length === 0 ? (
                 <span className="text-slate-600 italic">No execution in progress...</span>
               ) : (
                 executionLogs.map((log, i) => <div key={i}>{'>'} {log}</div>)
               )}
               <div ref={logsEndRef} />
             </div>
          </section>
        </div>

        {/* Right Column: HITL Plan */}
        <div>
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-medium flex items-center gap-2">
                <Database className="w-5 h-5 text-cyan-400" />
                Human-in-the-Loop Approval
              </h2>
              {plan && (
                <span className="text-xs bg-slate-800 px-2 py-1 rounded text-slate-400 border border-slate-700">
                  {plan.length} Tables Resolved
                </span>
              )}
            </div>

            <div className="flex-1 bg-slate-950 border border-slate-800 rounded-lg p-4 overflow-y-auto mb-6">
              {!plan ? (
                <div className="h-full flex items-center justify-center text-slate-600 text-sm italic">
                  Compile a plan to see resolved dependencies here.
                </div>
              ) : (
                <AnimatePresence>
                  <ul className="space-y-2">
                    {plan.map(table => (
                      <motion.li 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        key={table} 
                        className="flex justify-between items-center bg-slate-900 border border-slate-800 px-4 py-2 rounded-md group hover:border-slate-700 transition-colors"
                      >
                        <span className="font-mono text-sm text-slate-300">{table}</span>
                        <button 
                          onClick={() => handleRemoveTable(table)}
                          className="text-slate-500 hover:text-red-400 transition-colors"
                          disabled={executing}
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </motion.li>
                    ))}
                  </ul>
                </AnimatePresence>
              )}
            </div>

            <button 
              onClick={handleExecute}
              disabled={!plan || plan.length === 0 || executing}
              className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Play className="w-5 h-5 fill-current" /> Execute Pipeline
            </button>
          </section>
        </div>

      </main>
    </div>
  )
}

export default App
