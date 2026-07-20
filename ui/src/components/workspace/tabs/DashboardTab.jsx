import React from 'react';
import { Activity, Database, Code2, CheckCircle2, AlertTriangle, XCircle, History, Table2, FileText, ServerCog, Zap } from 'lucide-react';
import ActionToolbar from '../../common/ActionToolbar';
import { useLiveData } from '../../../hooks/useLiveData';
import { ENDPOINTS } from '../../../api/endpoints';

// ── Compact pipeline — Azure DevOps style ─────────────────────────────────────
const STAGES = ['Connect', 'Analyze', 'Convert', 'Validate', 'Deploy'];

function Pipeline({ stageIndex = 0, progress = 0 }) {
  return (
    <div style={{ borderBottom: '1px solid var(--color-border)', padding: '12px 16px', flexShrink: 0 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
        {STAGES.map((stage, i) => {
          const done    = i < stageIndex;
          const active  = i === stageIndex;
          const pending = i > stageIndex;
          return (
            <React.Fragment key={stage}>
              {/* Stage node */}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3, minWidth: 64 }}>
                <div style={{
                  width: 20, height: 20, borderRadius: '50%', border: '2px solid',
                  borderColor: done ? 'var(--color-success)' : active ? 'var(--color-primary)' : 'var(--color-border)',
                  background: done ? 'rgba(34,197,94,0.15)' : active ? 'rgba(37,99,235,0.15)' : 'transparent',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>
                  {done   && <CheckCircle2 style={{ width: 10, height: 10, color: 'var(--color-success)' }} />}
                  {active && <div style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--color-primary)' }} />}
                </div>
                <span style={{
                  fontSize: 10, fontWeight: active ? 600 : 400, letterSpacing: '0.05em',
                  color: done ? 'var(--color-success)' : active ? 'var(--color-primary)' : 'var(--color-muted)',
                  textTransform: 'uppercase',
                }}>
                  {stage}
                </span>
              </div>
              {/* Connector line */}
              {i < STAGES.length - 1 && (
                <div style={{
                  flex: 1, height: 1, marginBottom: 18,
                  background: done ? 'var(--color-success)' : 'var(--color-border)',
                }} />
              )}
            </React.Fragment>
          );
        })}
      </div>
      {/* Progress bar */}
      <div style={{ marginTop: 8, height: 2, background: 'var(--color-border)' }}>
        <div style={{ height: 2, background: 'var(--color-primary)', width: `${progress}%`, transition: 'width 600ms ease' }} />
      </div>
    </div>
  );
}

// ── Compact info bar — replaces 4 big cards ───────────────────────────────────
function InfoBar({ stats }) {
  const items = [
    { label: 'Objects',    value: stats?.objects    ?? '—', color: 'var(--color-text)' },
    { label: 'Tables',     value: stats?.tables     ?? '—', color: 'var(--color-text)' },
    { label: 'Views',      value: stats?.views      ?? '—', color: 'var(--color-text)' },
    { label: 'Packages',   value: stats?.packages   ?? '—', color: 'var(--color-text)' },
    { label: 'Converted',  value: stats?.converted  != null ? `${stats.converted}%`  : '—', color: 'var(--color-success)' },
    { label: 'Validated',  value: stats?.validated  != null ? `${stats.validated}%`  : '—', color: 'var(--color-success)' },
    { label: 'Errors',     value: stats?.errors     ?? '—', color: stats?.errors > 0 ? 'var(--color-error)'   : 'var(--color-success)' },
    { label: 'Warnings',   value: stats?.warnings   ?? '—', color: stats?.warnings > 0 ? 'var(--color-warning)' : 'var(--color-text)'    },
    { label: 'Last Run',   value: stats?.last_run   ?? '—', color: 'var(--color-muted)' },
  ];

  return (
    <div style={{
      display: 'flex', borderBottom: '1px solid var(--color-border)', flexShrink: 0,
      background: 'var(--color-panel)',
    }}>
      {items.map(({ label, value, color }, i) => (
        <div key={label} style={{
          flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
          height: 48, borderRight: i < items.length - 1 ? '1px solid var(--color-border)' : 'none',
          gap: 2, padding: '0 8px',
        }}>
          <span style={{ fontSize: 14, fontWeight: 700, color }}>{value}</span>
          <span style={{ fontSize: 11, color: 'var(--color-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</span>
        </div>
      ))}
    </div>
  );
}

// ── Flat section header ────────────────────────────────────────────────────────
function SectionHeader({ icon: Icon, label, iconColor }) {
  return (
    <div style={{
      height: 28, display: 'flex', alignItems: 'center', padding: '0 12px', gap: 6,
      fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em',
      color: 'var(--color-muted)', background: 'var(--color-bg)',
      borderBottom: '1px solid var(--color-border)', flexShrink: 0,
    }}>
      {Icon && <Icon style={{ width: 12, height: 12, color: iconColor ?? 'var(--color-muted)' }} />}
      {label}
    </div>
  );
}

// ── Flat data row ──────────────────────────────────────────────────────────────
function DataRow({ label, value, valueColor, meta }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      height: 28, padding: '0 12px', borderBottom: '1px solid var(--color-border)',
      fontSize: 12,
    }}>
      <span style={{ color: 'var(--color-muted)' }}>{label}</span>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        {meta && <span style={{ color: 'var(--color-muted)', fontSize: 11 }}>{meta}</span>}
        <span style={{ color: valueColor ?? 'var(--color-text)', fontWeight: 500, fontVariantNumeric: 'tabular-nums' }}>{value}</span>
      </div>
    </div>
  );
}

// ── Recent Projects ────────────────────────────────────────────────────────────
function ProjectRow({ project }) {
  const statusColor = {
    in_progress: 'var(--color-primary)',
    completed:   'var(--color-success)',
    pending:     'var(--color-muted)',
  }[project.status] ?? 'var(--color-muted)';

  return (
    <div style={{
      display: 'flex', alignItems: 'center', height: 28,
      padding: '0 12px', borderBottom: '1px solid var(--color-border)',
      fontSize: 12, gap: 8,
    }}>
      <span style={{ width: 6, height: 6, borderRadius: '50%', background: statusColor, flexShrink: 0 }} />
      <span style={{ flex: 1, color: 'var(--color-text)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
        {project.name}
      </span>
      <span style={{ color: 'var(--color-muted)', fontSize: 11, flexShrink: 0 }}>{project.last_updated}</span>
      <span style={{ color: statusColor, fontSize: 11, fontWeight: 600, flexShrink: 0, minWidth: 40, textAlign: 'right' }}>
        {project.progress}%
      </span>
    </div>
  );
}

// ── Main Dashboard ─────────────────────────────────────────────────────────────
export default function DashboardTab() {
  // Live data — polls every 30s
  const { data: status,   loading: loadingStatus }   = useLiveData(ENDPOINTS.MIGRATION_STATUS, 30000);
  const { data: stats,    loading: loadingStats }     = useLiveData(ENDPOINTS.MIGRATION_STATS,  30000);
  const { data: projects, loading: loadingProjects }  = useLiveData(ENDPOINTS.PROJECTS,         60000);

  const stageIndex = status?.stage_index    ?? 2;
  const progress   = status?.progress       ?? 0;
  const projectList= projects?.projects     ?? [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: 'var(--color-bg)', overflow: 'hidden' }}>

      {/* Toolbar */}
      <ActionToolbar
        title="Command Center"
        type="DASHBOARD"
        loading={loadingStatus || loadingStats}
      />

      {/* Migration Pipeline — compact, no card */}
      <Pipeline stageIndex={stageIndex} progress={progress} />

      {/* Info bar — replaces the 4 big stat cards */}
      <InfoBar stats={stats} />

      {/* Content — two columns, flat tables */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* Left column — Object Stats */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--color-border)', overflow: 'hidden' }}>
          <SectionHeader icon={Database} label="Object Statistics" iconColor="var(--color-warning)" />
          <div style={{ flex: 1, overflowY: 'auto' }}>
            <DataRow label="Tables"       value={stats?.tables      ?? '—'} />
            <DataRow label="Views"        value={stats?.views       ?? '—'} />
            <DataRow label="Packages"     value={stats?.packages    ?? '—'} />
            <DataRow label="Functions"    value={stats?.functions   ?? '—'} />
            <DataRow label="Converted"    value={stats?.converted   != null ? `${stats.converted}%` : '—'} valueColor="var(--color-success)" />
            <DataRow label="Validated"    value={stats?.validated   != null ? `${stats.validated}%` : '—'} valueColor="var(--color-success)" />
            <DataRow label="Errors"       value={stats?.errors      ?? '—'} valueColor={stats?.errors > 0 ? 'var(--color-error)' : 'var(--color-success)'} />
            <DataRow label="Warnings"     value={stats?.warnings    ?? '—'} valueColor={stats?.warnings > 0 ? 'var(--color-warning)' : 'var(--color-text)'} />
            <DataRow label="Last Run"     value={stats?.last_run    ?? '—'} valueColor="var(--color-muted)" />
          </div>
        </div>

        {/* Right column — Recent Projects */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <SectionHeader icon={History} label="Recent Projects" iconColor="var(--color-primary)" />
          <div style={{ flex: 1, overflowY: 'auto' }}>
            {loadingProjects
              ? <div style={{ padding: 16, fontSize: 12, color: 'var(--color-muted)' }}>Loading…</div>
              : projectList.length === 0
                ? <div style={{ padding: 16, fontSize: 12, color: 'var(--color-muted)', fontStyle: 'italic' }}>No projects found.</div>
                : projectList.map(p => <ProjectRow key={p.id} project={p} />)
            }
          </div>
        </div>

      </div>
    </div>
  );
}
