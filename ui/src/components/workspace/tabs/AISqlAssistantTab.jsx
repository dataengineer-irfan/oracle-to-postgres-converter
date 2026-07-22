import React, { useState } from 'react';
import { Play, Sparkles, AlertCircle, CheckCircle2, Database, MessageSquare, Copy, Download } from 'lucide-react';
import client from '../../../api/client';
import { ENDPOINTS } from '../../../api/endpoints';

export default function AISqlAssistantTab() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedSql, setGeneratedSql] = useState('-- Generated PostgreSQL will appear here.\n-- Type a request above and click Generate SQL.');
  
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  const [executionError, setExecutionError] = useState('');

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    setGeneratedSql('');
    setExecutionResult(null);
    setExecutionError('');
    
    try {
      const res = await client.post(ENDPOINTS.AI_SQL_GENERATE, { prompt });
      setGeneratedSql(res.data.sql);
    } catch (err) {
      setExecutionError(err.response?.data?.detail || err.message || 'Failed to generate SQL');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExecute = async () => {
    if (!generatedSql) return;
    
    setIsExecuting(true);
    setExecutionResult(null);
    setExecutionError('');
    
    try {
      const res = await client.post(ENDPOINTS.SQL_EXECUTE, { sql: generatedSql });
      setExecutionResult(res.data);
    } catch (err) {
      setExecutionError(err.response?.data?.detail || err.message || 'Execution failed');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedSql);
  };
  const handleDownload = () => {
    const blob = new Blob([generatedSql], { type: 'text/sql' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'query.sql';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ padding: '24px', height: '100%', overflowY: 'auto' }}>
      
      <div style={{ marginBottom: '24px', borderBottom: '1px solid var(--color-border)', paddingBottom: '16px' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Sparkles size={20} color="var(--color-primary)" />
          AI SQL Assistant
        </h2>
        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem', marginTop: '4px' }}>
          Type a natural language request. The AI will translate it to PostgreSQL and let you execute it safely.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '800px' }}>
        
        {/* Prompt Input */}
        <form onSubmit={handleGenerate} style={{ display: 'flex', gap: '12px' }}>
          <div style={{ flex: 1, position: 'relative' }}>
            <MessageSquare size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--color-text-muted)' }} />
            <input
              type="text"
              placeholder="e.g. Update p_dba_nam to 'testname' in p_dtl_tb where sys_id is 3163961"
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              disabled={isGenerating || isExecuting}
              style={{
                width: '100%',
                padding: '10px 16px 10px 36px',
                background: 'var(--color-bg)',
                border: '1px solid var(--color-border)',
                color: 'var(--color-text)',
                borderRadius: '6px',
                fontSize: '0.875rem'
              }}
            />
          </div>
          <button
            type="submit"
            disabled={isGenerating || isExecuting || !prompt.trim()}
            style={{
              padding: '0 20px',
              background: 'var(--color-primary)',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: (isGenerating || !prompt.trim()) ? 'not-allowed' : 'pointer',
              opacity: (isGenerating || !prompt.trim()) ? 0.7 : 1,
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontWeight: 500
            }}
          >
            {isGenerating ? 'Thinking...' : 'Generate SQL'}
          </button>
        </form>

        {/* Generated SQL */}
        <div style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', borderRadius: '8px', overflow: 'hidden' }}>
          <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--color-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>
              Generated PostgreSQL
            </span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                onClick={handleCopy}
                style={{
                  background: 'transparent', color: 'var(--color-text-muted)', border: '1px solid var(--color-border)',
                  padding: '6px 10px', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem'
                }}
                title="Copy SQL"
              >
                <Copy size={14} /> Copy
              </button>
              <button
                onClick={handleDownload}
                style={{
                  background: 'transparent', color: 'var(--color-text-muted)', border: '1px solid var(--color-border)',
                  padding: '6px 10px', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem'
                }}
                title="Download SQL"
              >
                <Download size={14} /> Download
              </button>
              <button
                onClick={handleExecute}
                disabled={isExecuting || !generatedSql.trim() || generatedSql.startsWith('-- Generated PostgreSQL')}
                style={{
                  background: 'var(--color-success)',
                  color: 'white',
                  border: 'none',
                  padding: '6px 12px',
                  borderRadius: '4px',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  cursor: (isExecuting || !generatedSql.trim() || generatedSql.startsWith('-- Generated PostgreSQL')) ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  opacity: (isExecuting || !generatedSql.trim() || generatedSql.startsWith('-- Generated PostgreSQL')) ? 0.7 : 1
                }}
              >
                <Play size={14} fill="currentColor" />
                {isExecuting ? 'Executing...' : 'Run Query'}
              </button>
            </div>
          </div>
          <div style={{ padding: '0' }}>
            <textarea
              value={generatedSql}
              onChange={e => setGeneratedSql(e.target.value)}
              style={{ 
                margin: 0, 
                width: '100%', 
                minHeight: '80px',
                fontFamily: 'monospace', 
                fontSize: '0.875rem', 
                color: '#e2e8f0', 
                background: 'var(--color-bg)',
                border: 'none',
                padding: '16px',
                resize: 'vertical',
                outline: 'none'
              }}
            />
          </div>
        </div>

        {/* Execution Error */}
        {executionError && (
          <div style={{ padding: '16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--color-error)', borderRadius: '8px', color: 'var(--color-error)', display: 'flex', gap: '12px' }}>
            <AlertCircle size={20} style={{ flexShrink: 0 }} />
            <div style={{ fontSize: '0.875rem', wordBreak: 'break-word' }}>
              {executionError}
            </div>
          </div>
        )}

        {/* Execution Success */}
        {executionResult && (
          <div style={{ border: '1px solid var(--color-border)', borderRadius: '8px', overflow: 'hidden' }}>
            <div style={{ padding: '12px 16px', background: 'rgba(34, 197, 94, 0.1)', borderBottom: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-success)' }}>
              <CheckCircle2 size={18} />
              <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>
                Query executed successfully. ({executionResult.rowcount} rows affected)
              </span>
            </div>
            
            {/* Render Select Data if available */}
            {executionResult.columns && executionResult.columns.length > 0 && (
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8125rem' }}>
                  <thead style={{ background: 'var(--color-bg)' }}>
                    <tr>
                      {executionResult.columns.map(col => (
                        <th key={col} style={{ padding: '8px 16px', textAlign: 'left', borderBottom: '1px solid var(--color-border)', color: 'var(--color-text-muted)' }}>
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {executionResult.rows.map((row, i) => (
                      <tr key={i} style={{ borderBottom: '1px solid var(--color-border)' }}>
                        {row.map((cell, j) => (
                          <td key={j} style={{ padding: '8px 16px', whiteSpace: 'nowrap' }}>
                            {cell === null ? <span style={{ color: 'var(--color-text-muted)', fontStyle: 'italic' }}>null</span> : String(cell)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
        
      </div>
    </div>
  );
}
