import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Terminal, Database, Play, RefreshCw, X, AlertTriangle, ListTree, Table2, GripHorizontal } from 'lucide-react';
import { useStore } from '../../../store/useStore';
import ActionToolbar from '../../common/ActionToolbar';

export default function DataGeneratorTab({ tab }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [plan, setPlan] = useState(null);
  const wsRef = useRef(null);
  
  const addLog = useStore(state => state.addLog);

  const handleParse = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8080/parse-intent', { prompt });
      setPlan(res.data.plan);
      addLog({ level: 'INFO', module: 'AI Generator', message: `Parsed intent. Found ${res.data.plan.length} tables to generate.` });
    } catch (err) {
      addLog({ level: 'ERROR', module: 'AI Generator', message: 'Failed to parse intent. Is the backend running?' });
    }
    setLoading(false);
  };

  const handleRemoveTable = (table) => {
    setPlan(plan.filter(t => t !== table));
  };

  const handleExecute = async () => {
    if (!plan || plan.length === 0) return;
    setExecuting(true);
    addLog({ level: 'INFO', module: 'Data Pipeline', message: 'Connecting to execution WebSocket...' });
    
    // Connect to WebSocket
    wsRef.current = new WebSocket('ws://localhost:8080/ws/logs');
    wsRef.current.onmessage = (event) => {
      addLog({ level: 'INFO', module: 'Data Pipeline', message: event.data });
      if (event.data.includes("Pipeline finished")) {
        setExecuting(false);
        wsRef.current.close();
      }
    };

    try {
      await axios.post('http://localhost:8080/execute', { tables: plan, rows: 50 });
      addLog({ level: 'INFO', module: 'Data Pipeline', message: 'Execution started.' });
    } catch (err) {
      addLog({ level: 'ERROR', module: 'Data Pipeline', message: 'Failed to start execution.' });
      setExecuting(false);
      if (wsRef.current) wsRef.current.close();
    }
  };

  return (
    <div className="h-full flex flex-col bg-bg overflow-hidden text-text">
      <ActionToolbar title="DML Generation" type="AI PIPELINE" onCopy={() => {}} onDownload={() => {}} />
      
      <div className="flex-1 flex flex-col lg:flex-row overflow-y-auto custom-scrollbar p-6 gap-6">
        {/* Left Column: Input */}
        <div className="flex-1 space-y-6">
          <section className="bg-panel border border-border rounded shadow-lg overflow-hidden">
            <div className="bg-bg/50 border-b border-border px-4 py-3 flex items-center text-sm font-semibold">
              <Terminal className="w-4 h-4 mr-2 text-primary" />
              Natural Language DML Prompt
            </div>
            <div className="p-4">
              <textarea 
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g., Generate 50 records for provider addresses and taxonomy..."
                className="w-full h-40 bg-bg border border-border rounded p-4 text-text focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all resize-none mb-4 font-mono text-sm"
              />
              <button 
                onClick={handleParse}
                disabled={loading || executing}
                className="w-full bg-primary hover:bg-primary/90 text-bg font-semibold py-2 px-4 rounded flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : 'Compile DML Plan'}
              </button>
            </div>
          </section>

          {/* Metadata Section */}
          {plan && (
            <section className="bg-panel border border-border rounded shadow-lg overflow-hidden">
               <div className="bg-bg/50 border-b border-border px-4 py-3 flex items-center text-sm font-semibold">
                  <Database className="w-4 h-4 mr-2 text-info" />
                  Generation Metadata
               </div>
               <div className="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="flex flex-col border border-border rounded p-3 bg-bg items-center justify-center text-center">
                    <GripHorizontal className="w-4 h-4 text-primary mb-1" />
                    <span className="text-xl font-bold">50</span>
                    <span className="text-[10px] text-muted uppercase tracking-wider">Target Rows</span>
                  </div>
                  <div className="flex flex-col border border-border rounded p-3 bg-bg items-center justify-center text-center">
                    <Table2 className="w-4 h-4 text-success mb-1" />
                    <span className="text-xl font-bold">{plan.length}</span>
                    <span className="text-[10px] text-muted uppercase tracking-wider">Tables</span>
                  </div>
                  <div className="flex flex-col border border-border rounded p-3 bg-bg items-center justify-center text-center">
                    <ListTree className="w-4 h-4 text-info mb-1" />
                    <span className="text-xl font-bold">{plan.length * 2 - 1}</span>
                    <span className="text-[10px] text-muted uppercase tracking-wider">Dependencies</span>
                  </div>
                  <div className="flex flex-col border border-border rounded p-3 bg-bg items-center justify-center text-center">
                    <AlertTriangle className="w-4 h-4 text-warning mb-1" />
                    <span className="text-xl font-bold">0</span>
                    <span className="text-[10px] text-muted uppercase tracking-wider">Warnings</span>
                  </div>
               </div>
            </section>
          )}
        </div>

        {/* Right Column: HITL Plan */}
        <div className="w-full lg:w-96 flex flex-col">
          <section className="bg-panel border border-border rounded shadow-lg flex-1 flex flex-col overflow-hidden">
            <div className="bg-bg/50 border-b border-border px-4 py-3 flex justify-between items-center text-sm font-semibold">
              <div className="flex items-center">
                <Database className="w-4 h-4 text-success mr-2" />
                Human-in-the-Loop Plan
              </div>
              {plan && (
                <span className="text-[10px] bg-primary/20 text-primary px-1.5 py-0.5 rounded font-bold">
                  {plan.length} TABLES
                </span>
              )}
            </div>

            <div className="flex-1 bg-bg p-4 overflow-y-auto custom-scrollbar min-h-[200px]">
              {!plan ? (
                <div className="h-full flex items-center justify-center text-muted text-xs italic">
                  Compile a plan to see resolved dependencies here.
                </div>
              ) : (
                <ul className="space-y-2">
                  {plan.map(table => (
                    <li 
                      key={table} 
                      className="flex justify-between items-center bg-panel border border-border px-3 py-2 rounded text-xs group hover:border-primary/50 transition-colors"
                    >
                      <span className="font-mono text-text">{table}</span>
                      <button 
                        onClick={() => handleRemoveTable(table)}
                        className="text-muted hover:text-error transition-colors"
                        disabled={executing}
                        title="Remove Table from Pipeline"
                      >
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="p-4 bg-bg/50 border-t border-border">
              <button 
                onClick={handleExecute}
                disabled={!plan || plan.length === 0 || executing}
                className="w-full bg-success hover:bg-success/90 text-bg font-semibold py-3 px-4 rounded flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-success/20"
              >
                <Play className="w-5 h-5 fill-current" /> Execute Pipeline
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
