import React, { useState } from 'react';
import { BrainCircuit, AlertTriangle, Lightbulb, Info, ChevronRight, ChevronDown } from 'lucide-react';
import { useLiveData } from '../../hooks/useLiveData';
import { ENDPOINTS } from '../../api/endpoints';

// Flat metric row
function MetricRow({ label, value, valueColor }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 24, padding: '0 8px', fontSize: 11, borderBottom: '1px solid var(--color-border)', cursor: 'default' }} className="hover:bg-border transition-colors">
      <span style={{ color: 'var(--color-muted)' }}>{label}</span>
      <span style={{ color: valueColor ?? 'var(--color-text)', fontWeight: 500 }}>{value}</span>
    </div>
  );
}

function InspectorTab({ id, label, active, onClick }) {
  return (
    <button
      onClick={() => onClick(id)}
      style={{
        padding: '0 6px', height: 24, fontSize: 11, cursor: 'pointer', border: 'none',
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

// Collapsible Section wrapper
function ExpandableSection({ icon: Icon, title, iconColor, defaultOpen = true, children }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between hover:bg-border transition-colors"
        style={{ 
          border: 'none', borderBottom: '1px solid var(--color-border)', 
          height: 24, padding: '0 8px', fontSize: 10, cursor: 'pointer', 
          background: 'var(--color-bg)', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-muted)' 
        }}
      >
        <div className="flex items-center">
          {Icon && <Icon style={{ width: 12, height: 12, marginRight: 6, color: iconColor }} />}
          <span style={{ fontWeight: 600 }}>{title}</span>
        </div>
        {isOpen ? <ChevronDown style={{ width: 12, height: 12, color: 'var(--color-muted)' }} /> : <ChevronRight style={{ width: 12, height: 12, color: 'var(--color-muted)' }} />}
      </button>
      {isOpen && (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {children}
        </div>
      )}
    </div>
  );
}

export default function AiIntelligence() {
  const [activeTab, setActiveTab] = useState('overview');

  const { data: analysis } = useLiveData(ENDPOINTS.AI_ANALYSIS, 60000);

  const confidence      = analysis?.confidence      ?? 0;
  const objectsAnalyzed = analysis?.objects_analyzed ?? 0;
  const autoConverted   = analysis?.auto_converted   ?? 0;
  const manualHours     = analysis?.manual_hours      ?? 0;
  const warnings        = analysis?.warnings          ?? 0;
  const errors          = analysis?.errors            ?? 0;

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
      overflowY: 'auto', overflowX: 'hidden', flexShrink: 0,
    }}>

      {/* Header */}
      <div className="ide-section-header" style={{ flexShrink: 0, height: 28 }}>
        <BrainCircuit style={{ width: 14, height: 14, marginRight: 6, color: 'var(--color-primary)' }} />
        AI Intelligence
      </div>

      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 12px', height: 26, flexShrink: 0,
        borderBottom: '1px solid var(--color-border)',
        background: 'var(--color-bg)',
      }}>
        <span style={{ fontSize: 11, color: 'var(--color-muted)' }}>Confidence Score</span>
        <span style={{ fontSize: 11, color: 'var(--color-success)', fontWeight: 600 }}>{confidence}%</span>
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
      <div style={{ flex: 1, overflow: 'visible' }}>

        {activeTab === 'overview' && (
          <>
            {/* Migration Summary */}
            <ExpandableSection title="Migration Summary">
              <MetricRow label="Objects Analyzed"  value={objectsAnalyzed.toLocaleString()} />
              <MetricRow label="Auto-Converted"    value={`${autoConverted.toLocaleString()} (${objectsAnalyzed > 0 ? Math.round(autoConverted/objectsAnalyzed*100) : 0}%)`} valueColor="var(--color-success)" />
              <MetricRow label="Manual Effort"     value={`~${manualHours}h`} valueColor="var(--color-warning)" />
              <MetricRow label="Warnings"          value={warnings} valueColor={warnings > 0 ? 'var(--color-warning)' : 'var(--color-success)'} />
              <MetricRow label="Errors"            value={errors}   valueColor={errors   > 0 ? 'var(--color-error)'   : 'var(--color-success)'} />
            </ExpandableSection>

            {/* Unsupported features */}
            <ExpandableSection icon={AlertTriangle} iconColor="var(--color-warning)" title="Unsupported Features">
              {[
                'DBMS_CRYPTO → pgcrypto required',
                'XMLType → JSONB recommended',
                'DBMS_SCHEDULER → pg_cron',
              ].map((item, i) => (
                <div key={i} style={{
                  padding: '2px 8px', fontSize: 10.5,
                  color: 'var(--color-muted)', borderBottom: '1px solid var(--color-border)',
                  borderLeft: '2px solid var(--color-warning)',
                }}>
                  {item}
                </div>
              ))}
            </ExpandableSection>

            {/* Suggestion */}
            <ExpandableSection icon={Lightbulb} iconColor="var(--color-primary)" title="Top Suggestion">
              <div style={{ padding: '6px 8px', fontSize: 10.5, color: 'var(--color-muted)', lineHeight: '14px', borderBottom: '1px solid var(--color-border)' }}>
                Replace SEQ_PROVIDER_ID.NEXTVAL trigger with a native PostgreSQL IDENTITY column.
                <br/>
                Est. performance gain: <span style={{ color: 'var(--color-success)', fontWeight: 500 }}>+14%</span>
              </div>
            </ExpandableSection>
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
