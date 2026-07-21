import React, { useState, useRef } from 'react';
import { Terminal, Database, Play, RefreshCw, X, AlertTriangle, ListTree, Table2, ArrowLeft, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import TopHeader from '../components/layout/TopHeader';
import ActionToolbar from '../components/common/ActionToolbar';
import PermissionGate from '../rbac/PermissionGate';
import { ENDPOINTS } from '../api/endpoints';
import client from '../api/client';
import { useStore } from '../store/useStore';
import AISqlAssistantTab from '../components/workspace/tabs/AISqlAssistantTab';

export default function DataGenerator() {
  const navigate  = useNavigate();
  const addLog    = useStore(s => s.addLog);

  const [activeMode, setActiveMode] = useState('data_gen'); // 'data_gen' | 'ai_sql'

  const [prompt,    setPrompt]   = useState('');
  const [parsing,   setParsing]  = useState(false);
  const [executing, setExecuting]= useState(false);
  const [plan,      setPlan]     = useState(null);
  const [targetRows, setTargetRows] = useState(5);
  const [logs,      setLogs]     = useState([]);
  const [downloading, setDownloading] = useState(false);
  const [copying,     setCopying]     = useState(false);
  const wsRef     = useRef(null);
  const logsEndRef= useRef(null);

  const appendLog = (msg, level = 'INFO') => {
    const entry = { text: msg, level, time: new Date().toLocaleTimeString() };
    setLogs(prev => {
      const next = [...prev, entry];
      setTimeout(() => logsEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 50);
      return next;
    });
    addLog({ level, module: 'DataGen', message: msg });
  };

  const handleParse = async () => {
    if (!prompt.trim()) return;
    setParsing(true);
    try {
      const res = await client.post(ENDPOINTS.PARSE_INTENT, { prompt });
      setPlan(res.data.plan);
      appendLog(`Parsed intent. Found ${res.data.plan.length} tables.`, 'SUCCESS');
    } catch {
      appendLog('Failed to parse intent. Is the backend running?', 'ERROR');
    }
    setParsing(false);
  };

  const handleExecute = async () => {
    if (!plan?.length) return;
    setExecuting(true);
    appendLog('Connecting to execution pipeline...', 'INFO');

    wsRef.current = new WebSocket(ENDPOINTS.WS_LOGS);
    wsRef.current.onmessage = (e) => {
      appendLog(e.data, 'INFO');
      if (e.data.includes('Pipeline finished') || e.data.includes('Complete')) {
        setExecuting(false);
        wsRef.current?.close();
      }
    };
    wsRef.current.onerror = () => {
      appendLog('WebSocket error. Check backend.', 'ERROR');
      setExecuting(false);
    };

    try {
      await client.post(ENDPOINTS.EXECUTE_PIPELINE, { tables: plan, rows: targetRows });
      appendLog('Pipeline started.', 'INFO');
    } catch {
      appendLog('Failed to start pipeline.', 'ERROR');
      setExecuting(false);
      wsRef.current?.close();
    }
  };

  const handleDownload = async (format) => {
    setDownloading(true);
    appendLog(`Generating ${format.toUpperCase()} download...`, 'INFO');
    await new Promise(r => setTimeout(r, 800)); // simulate
    appendLog(`Download ready: output.${format}`, 'SUCCESS');
    setDownloading(false);
  };

  const handleCopy = async (format) => {
    setCopying(true);
    appendLog(`Copying as ${format.toUpperCase()}...`, 'INFO');
    try {
      let textToCopy = '';
      if (format === 'all') {
         textToCopy = logs.map(l => `[${l.level}] ${l.time} ${l.text}`).join('\n') || 'No logs available.';
      } else if (format === 'sql' || format === 'dml') {
         if (plan && plan.length > 0) {
           try {
             const res = await client.post(ENDPOINTS.PREVIEW_DML, { tables: plan });
             textToCopy = res.data.dml || '-- No data generated yet.';
           } catch (e) {
             textToCopy = '-- Error fetching DML preview. Have you run the pipeline?';
           }
         } else {
           textToCopy = '-- No tables in plan.';
         }
      } else if (format === 'ddl') {
         textToCopy = (plan || []).map(t => `CREATE TABLE ${t} (\n  id SERIAL PRIMARY KEY\n);`).join('\n\n') || '-- No tables in plan.';
      } else if (format === 'json') {
         textToCopy = JSON.stringify({ plan: plan || [], targetRows: 50 }, null, 2);
      } else if (format === 'csv') {
         textToCopy = (plan || []).join(',\n') || 'No tables';
      } else {
         textToCopy = logs.map(l => `[${l.level}] ${l.time} ${l.text}`).join('\n') || 'No logs available.';
      }

      // Robust copy fallback for non-secure contexts
      if (navigator?.clipboard?.writeText) {
        await navigator.clipboard.writeText(textToCopy);
      } else {
        const textArea = document.createElement("textarea");
        textArea.value = textToCopy;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
          document.execCommand('copy');
        } catch (err) {
          throw new Error("execCommand failed");
        } finally {
          textArea.remove();
        }
      }
      appendLog(`Copied to clipboard.`, 'SUCCESS');
    } catch (err) {
      appendLog(`Failed to copy to clipboard.`, 'ERROR');
    }
    setCopying(false);
  };

  const logColor = (level) => {
    if (level === 'ERROR')   return 'var(--color-error)';
    if (level === 'SUCCESS') return 'var(--color-success)';
    if (level === 'WARNING') return 'var(--color-warning)';
    return 'var(--color-muted)';
  };

  return (
    <PermissionGate screen="data_generator">
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: 'var(--color-bg)', color: 'var(--color-text)', fontFamily: 'Inter, sans-serif', overflow: 'hidden' }}>
        <TopHeader />

        {/* Breadcrumb sub-header */}
        <div style={{
          height: 'var(--toolbar-h)', flexShrink: 0,
          display: 'flex', alignItems: 'center', padding: '0 12px', gap: 8,
          borderBottom: '1px solid var(--color-border)',
          background: 'var(--color-panel)', fontSize: 12,
        }}>
          <button className="btn-ghost" style={{ height: 24, padding: '0 8px', gap: 4, display: 'flex', alignItems: 'center', fontSize: 12 }}
                  onClick={() => navigate('/ide')}>
            <ArrowLeft style={{ width: 12, height: 12 }} />
            IDE
          </button>
          <span style={{ color: 'var(--color-border)' }}>›</span>
          <span 
            style={{ color: activeMode === 'data_gen' ? 'var(--color-primary)' : 'var(--color-text-muted)', cursor: 'pointer', fontWeight: activeMode === 'data_gen' ? 500 : 400 }} 
            onClick={() => setActiveMode('data_gen')}
          >
            Smart Test Data Generator
          </span>
          <span style={{ color: 'var(--color-border)' }}>|</span>
          <span 
            style={{ color: activeMode === 'ai_sql' ? 'var(--color-primary)' : 'var(--color-text-muted)', cursor: 'pointer', fontWeight: activeMode === 'ai_sql' ? 500 : 400 }} 
            onClick={() => setActiveMode('ai_sql')}
          >
            AI SQL Assistant
          </span>
        </div>

        {/* Toolbar */}
        <ActionToolbar
          title="DML Pipeline"
          type="DML"
          loading={copying || downloading}
          onCopy={handleCopy}
          onDownload={handleDownload}
          extra={
            <PermissionGate permission="execute_dml" overlay={false} fallback={null}>
              <button
                className="btn-primary"
                style={{ height: 24, padding: '0 10px', fontSize: 12, display: 'flex', alignItems: 'center', gap: 6 }}
                onClick={handleExecute}
                disabled={!plan?.length || executing}
              >
                {executing ? <Loader2 style={{ width: 12, height: 12, animation: 'spin 0.6s linear infinite' }} /> : <Play style={{ width: 12, height: 12 }} />}
                {executing ? 'Running…' : 'Execute Pipeline'}
              </button>
            </PermissionGate>
          }
        />

        {/* Main workspace */}
        <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
          {activeMode === 'ai_sql' ? (
            <div style={{ flex: 1, overflow: 'auto' }}>
              <AISqlAssistantTab />
            </div>
          ) : (
            <>
              {/* Left: Prompt + Logs */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--color-border)', overflow: 'hidden' }}>

            {/* Prompt section */}
            <div style={{ borderBottom: '1px solid var(--color-border)', flexShrink: 0 }}>
              <div className="ide-section-header">
                <Terminal style={{ width: 12, height: 12, marginRight: 6, color: 'var(--color-primary)' }} />
                Natural Language Prompt
              </div>
              <div style={{ padding: 12 }}>
                <textarea
                  value={prompt}
                  onChange={e => setPrompt(e.target.value)}
                  placeholder="e.g., Generate 50 records for providers with different types and specialities..."
                  spellCheck={false}
                  style={{
                    width: '100%', height: 96, padding: 8,
                    background: 'var(--color-bg)', border: '1px solid var(--color-border)',
                    borderRadius: 'var(--radius)', color: 'var(--color-text)',
                    fontFamily: 'JetBrains Mono, monospace', fontSize: 12, lineHeight: '18px',
                    resize: 'none', outline: 'none',
                    transition: 'border-color 150ms',
                  }}
                  onFocus={e => e.target.style.borderColor = 'var(--color-primary)'}
                  onBlur={e  => e.target.style.borderColor = 'var(--color-border)'}
                />
                <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
                  <div style={{ flexShrink: 0, display: 'flex', alignItems: 'center', background: 'var(--color-bg)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)', padding: '0 8px' }}>
                    <span style={{ fontSize: 12, color: 'var(--color-text-muted)', marginRight: 8 }}>Target Rows:</span>
                    <input 
                      type="number" 
                      min="1" 
                      max="1000" 
                      value={targetRows} 
                      onChange={e => setTargetRows(parseInt(e.target.value) || 1)} 
                      style={{ background: 'transparent', border: 'none', color: 'var(--color-text)', outline: 'none', fontSize: 13, width: '60px' }} 
                    />
                  </div>
                  <button
                    className="btn-primary"
                    style={{ flex: 1, height: 28, fontSize: 13, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}
                    onClick={handleParse}
                    disabled={parsing || executing}
                  >
                    {parsing
                      ? <><span className="ide-spinner" />  Compiling plan…</>
                      : 'Compile Data Generation Plan'
                    }
                  </button>
                </div>
              </div>
            </div>

            {/* Stats row — if plan exists */}
            {plan && (
              <div style={{
                display: 'flex', borderBottom: '1px solid var(--color-border)',
                flexShrink: 0,
              }}>
                {[
                  { label: 'Target Rows', value: targetRows, icon: Table2 },
                  { label: 'Tables',      value: plan.length, icon: Database },
                  { label: 'Dependencies',value: plan.length * 2 - 1, icon: ListTree },
                  { label: 'Warnings',    value: 0, icon: AlertTriangle },
                ].map(({ label, value, icon: Icon }) => (
                  <div key={label} style={{
                    flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                    height: 52, borderRight: '1px solid var(--color-border)', gap: 2,
                  }}>
                    <span style={{ fontSize: 16, fontWeight: 700, color: 'var(--color-text)' }}>{value}</span>
                    <span style={{ fontSize: 11, color: 'var(--color-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Execution Logs */}
            <div className="ide-section-header" style={{ flexShrink: 0, borderBottom: '1px solid var(--color-border)' }}>
              <Database style={{ width: 12, height: 12, marginRight: 6 }} />
              Execution Logs
            </div>
            <div style={{ flex: 1, overflowY: 'auto', padding: 8, fontFamily: 'JetBrains Mono, monospace', fontSize: 12, lineHeight: '20px' }}>
              {logs.length === 0
                ? <span style={{ color: 'var(--color-muted)', fontStyle: 'italic' }}>No active pipeline…</span>
                : logs.map((log, i) => (
                  <div key={i} style={{ display: 'flex', gap: 12 }}>
                    <span style={{ color: 'var(--color-border)', flexShrink: 0 }}>{log.time}</span>
                    <span style={{ color: logColor(log.level), flexShrink: 0, fontWeight: 600, width: 56 }}>[{log.level}]</span>
                    <span style={{ color: 'var(--color-text)' }}>{log.text}</span>
                  </div>
                ))
              }
              <div ref={logsEndRef} />
            </div>
          </div>

          {/* Right: HITL Approval */}
          <div style={{ width: 320, display: 'flex', flexDirection: 'column', flexShrink: 0, overflow: 'hidden' }}>
            <div className="ide-section-header" style={{ borderBottom: '1px solid var(--color-border)', justifyContent: 'space-between' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Database style={{ width: 12, height: 12, color: 'var(--color-success)' }} />
                Human-in-the-Loop Approval
              </span>
              {plan && <span style={{ fontSize: 11, color: 'var(--color-primary)' }}>{plan.length} tables</span>}
            </div>

            <div style={{ flex: 1, overflowY: 'auto', padding: plan ? 0 : 16 }}>
              {!plan
                ? <div style={{ textAlign: 'center', color: 'var(--color-muted)', fontSize: 12, fontStyle: 'italic', paddingTop: 32 }}>
                    Compile a plan to review dependencies.
                  </div>
                : plan.map(table => (
                  <div key={table} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '0 8px', height: 28,
                    borderBottom: '1px solid var(--color-border)',
                    fontSize: 12, fontFamily: 'JetBrains Mono, monospace',
                  }}>
                    <span style={{ color: 'var(--color-text)', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {table}
                    </span>
                    <button
                      className="btn-ghost"
                      style={{ width: 20, height: 20, padding: 0 }}
                      onClick={() => setPlan(plan.filter(t => t !== table))}
                      disabled={executing}
                      title="Remove from pipeline"
                    >
                      <X style={{ width: 11, height: 11 }} />
                    </button>
                  </div>
                ))
              }
            </div>

            {/* Execute CTA */}
            <PermissionGate permission="execute_dml" overlay={false} fallback={
              <div style={{ padding: 12, borderTop: '1px solid var(--color-border)', fontSize: 12, color: 'var(--color-muted)', textAlign: 'center' }}>
                Your role cannot execute DML pipelines.
              </div>
            }>
              <div style={{ padding: 12, borderTop: '1px solid var(--color-border)', flexShrink: 0 }}>
                <button
                  className="btn-primary"
                  style={{ width: '100%', height: 32, fontSize: 13, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6, background: 'var(--color-success)' }}
                  onClick={handleExecute}
                  disabled={!plan?.length || executing}
                >
                  {executing
                    ? <><span className="ide-spinner" /> Running…</>
                    : <><Play style={{ width: 14, height: 14 }} /> Execute Pipeline</>
                  }
                </button>
              </div>
            </PermissionGate>
          </div>
            </>
          )}
        </div>
      </div>
    </PermissionGate>
  );
}
