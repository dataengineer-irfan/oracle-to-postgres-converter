import React, { useState } from 'react';
import { BrainCircuit, AlertTriangle, Lightbulb, CheckCircle2, Info } from 'lucide-react';
import { useLiveData } from '../../hooks/useLiveData';
import { ENDPOINTS } from '../../api/endpoints';

// Flat metric row
function MetricRow({ label, value, valueColor }) {
  return (
    <div className="ide-metric-row">
      <span style={{ color: 'var(--color-muted)', fontSize: 12 }}>{label}</span>
      <span style={{ color: valueColor ?? 'var(--color-text)', fontSize: 12, fontWeight: 500 }}>{value}</span>
    </div>
  );
}

// Flat tab button
function InspectorTab({ id, label, active, onClick }) {
  return (
    <button
      onClick={() => onClick(id)}
      style={{
        padding: '0 10px', height: 28, fontSize: 12, cursor: 'pointer', border: 'none',
        background: 'transparent', whiteSpace: 'nowrap', fontWeight: active ? 600 : 400,
        color: active ? 'var(--color-text)' : 'var(--color-muted)',
        borderBottom: `2px solid ${active ? 'var(--color-primary)' : 'transparent'}`,
        transition: 'all 150ms',
      }}
    >
      {label}
    </button>
  );
}

export default function AiIntelligence() {
  const [activeTab, setActiveTab] = useState('overview');

  const { data: analysis } = useLiveData(ENDPOINTS.AI_ANALYSIS, 60000);

  const confidence      = analysis?.confidence      ?? 92;
  const objectsAnalyzed = analysis?.objects_analyzed ?? 14230;
  const autoConverted   = analysis?.auto_converted   ?? 13901;
  const manualHours     = analysis?.manual_hours      ?? 42;
  const warnings        = analysis?.warnings          ?? 12;
  const errors          = analysis?.errors            ?? 3;

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'analysis', label: 'Analysis' },
    { id: 'recs',     label: 'Recommendations' },
    { id: 'warnings', label: 'Warnings' },
  ];

  return (
    <div style={{
      width: 'var(--inspector-w)', height: '100%',
      background: 'var(--color-panel)',
      borderLeft: '1px solid var(--color-border)',
      display: 'flex', flexDirection: 'column',
      overflow: 'hidden', flexShrink: 0,
    }}>

      {/* Header */}
      <div className="ide-section-header" style={{ flexShrink: 0 }}>
        <BrainCircuit style={{ width: 14, height: 14, marginRight: 6, color: 'var(--color-primary)' }} />
        AI Intelligence
      </div>

      {/* Confidence — flat row, no card */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 8px', height: 32, flexShrink: 0,
        borderBottom: '1px solid var(--color-border)',
        background: 'var(--color-bg)',
      }}>
        <span style={{ fontSize: 12, color: 'var(--color-muted)' }}>Confidence Score</span>
        <span style={{ fontSize: 12, color: 'var(--color-success)', fontWeight: 600 }}>{confidence}%</span>
      </div>
      {/* Confidence bar — 2px, not a card */}
      <div style={{ height: 2, background: 'var(--color-border)', flexShrink: 0 }}>
        <div style={{ height: 2, background: 'var(--color-success)', width: `${confidence}%`, transition: 'width 300ms' }} />
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex', flexShrink: 0, overflowX: 'auto',
        borderBottom: '1px solid var(--color-border)',
        padding: '0 4px',
      }}>
        {tabs.map(t => (
          <InspectorTab key={t.id} id={t.id} label={t.label} active={activeTab === t.id} onClick={setActiveTab} />
        ))}
      </div>

      {/* Content — flat rows, no cards */}
      <div style={{ flex: 1, overflowY: 'auto' }}>

        {activeTab === 'overview' && (
          <>
            {/* Migration Summary */}
            <div className="ide-section-header" style={{ border: 'none', borderBottom: '1px solid var(--color-border)' }}>Migration Summary</div>
            <MetricRow label="Objects Analyzed"  value={objectsAnalyzed.toLocaleString()} />
            <MetricRow label="Auto-Converted"    value={`${autoConverted.toLocaleString()} (${Math.round(autoConverted/objectsAnalyzed*100)}%)`} valueColor="var(--color-success)" />
            <MetricRow label="Manual Effort"     value={`~${manualHours}h`} valueColor="var(--color-warning)" />
            <MetricRow label="Warnings"          value={warnings} valueColor={warnings > 0 ? 'var(--color-warning)' : 'var(--color-success)'} />
            <MetricRow label="Errors"            value={errors}   valueColor={errors   > 0 ? 'var(--color-error)'   : 'var(--color-success)'} />

            {/* Unsupported features */}
            <div className="ide-section-header" style={{ border: 'none', borderTop: '1px solid var(--color-border)', borderBottom: '1px solid var(--color-border)', marginTop: 8 }}>
              <AlertTriangle style={{ width: 12, height: 12, marginRight: 4, color: 'var(--color-warning)' }} />
              Unsupported Features
            </div>
            {[
              'DBMS_CRYPTO → pgcrypto required',
              'XMLType → JSONB recommended',
              'DBMS_SCHEDULER → pg_cron',
            ].map((item, i) => (
              <div key={i} style={{
                padding: '4px 8px 4px 12px', fontSize: 12,
                color: 'var(--color-muted)', borderBottom: '1px solid var(--color-border)',
                borderLeft: '2px solid var(--color-warning)', marginLeft: 8,
              }}>
                {item}
              </div>
            ))}

            {/* Suggestion */}
            <div className="ide-section-header" style={{ border: 'none', borderTop: '1px solid var(--color-border)', borderBottom: '1px solid var(--color-border)', marginTop: 8 }}>
              <Lightbulb style={{ width: 12, height: 12, marginRight: 4, color: 'var(--color-primary)' }} />
              Top Suggestion
            </div>
            <div style={{ padding: '6px 8px', fontSize: 12, color: 'var(--color-muted)', lineHeight: '18px' }}>
              Replace SEQ_PROVIDER_ID.NEXTVAL trigger with a native PostgreSQL IDENTITY column.
              Est. performance gain: <span style={{ color: 'var(--color-success)', fontWeight: 500 }}>+14%</span>
            </div>
          </>
        )}

        {activeTab !== 'overview' && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: 200, color: 'var(--color-muted)', gap: 8 }}>
            <Info style={{ width: 20, height: 20 }} />
            <span style={{ fontSize: 12 }}>Populates during active scan</span>
          </div>
        )}
      </div>
    </div>
  );
}
