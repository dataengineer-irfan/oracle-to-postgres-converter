import React, { useState } from 'react';
import { ChevronRight, ChevronDown, Database, Table2, LayoutGrid, Settings, History, AlertCircle, FileText, CheckSquare, ListTree } from 'lucide-react';
import { useStore } from '../../store/useStore';
import { useNavigate } from 'react-router-dom';
import { usePermissions } from '../../rbac/usePermissions';
import { useLiveData } from '../../hooks/useLiveData';
import { ENDPOINTS } from '../../api/endpoints';

// ── Tree Item ─────────────────────────────────────────────────────────────────
function TreeItem({ label, depth = 0, icon: Icon, children, defaultOpen = false, onClick, badge, dot }) {
  const [open, setOpen] = useState(defaultOpen);
  const hasChildren = !!children;

  return (
    <div>
      <div
        className="ide-tree-item"
        style={{ paddingLeft: 8 + depth * 12 }}
        onClick={() => { if (hasChildren) setOpen(o => !o); if (onClick) onClick(); }}
      >
        {/* Chevron */}
        <span style={{ width: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          {hasChildren
            ? open
              ? <ChevronDown style={{ width: 12, height: 12 }} />
              : <ChevronRight style={{ width: 12, height: 12 }} />
            : null}
        </span>
        {/* Status dot */}
        {dot && (
          <span style={{
            width: 6, height: 6, borderRadius: '50%', flexShrink: 0, marginRight: 4,
            background: dot === 'green' ? 'var(--color-success)' : 'var(--color-error)',
          }} />
        )}
        {/* Icon */}
        {Icon && <Icon style={{ width: 14, height: 14, marginRight: 4, flexShrink: 0, color: 'var(--color-primary)', opacity: 0.8 }} />}
        {/* Label */}
        <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{label}</span>
        {/* Badge */}
        {badge != null && (
          <span style={{ fontSize: 11, color: 'var(--color-muted)', marginLeft: 4, flexShrink: 0 }}>{badge}</span>
        )}
      </div>
      {open && hasChildren && (
        <div>{children}</div>
      )}
    </div>
  );
}

// ── Sidebar Section Header ────────────────────────────────────────────────────
function SectionHeader({ label }) {
  return (
    <div style={{
      height: 24, display: 'flex', alignItems: 'center',
      padding: '0 8px', fontSize: 11, fontWeight: 600,
      color: 'var(--color-muted)', textTransform: 'uppercase',
      letterSpacing: '0.08em', borderTop: '1px solid var(--color-border)',
      marginTop: 4,
    }}>
      {label}
    </div>
  );
}

// ── Main Sidebar ──────────────────────────────────────────────────────────────
export default function LeftSidebar() {
  const openTab = useStore(state => state.openTab);
  const navigate = useNavigate();
  const { can, hasScreen } = usePermissions();

  // Live schema counts
  const { data: oracleSchema } = useLiveData(ENDPOINTS.SCHEMA_ORACLE, 30000);
  const { data: pgSchema }     = useLiveData(ENDPOINTS.SCHEMA_POSTGRES, 30000);
  const { data: health }       = useLiveData(ENDPOINTS.CONNECTIONS_HEALTH, 10000);

  const oracleTables  = oracleSchema?.tables  ?? 420;
  const oracleViews   = oracleSchema?.views   ?? 62;
  const oraclePkgs    = oracleSchema?.packages ?? 18;
  const oracleIndexes = oracleSchema?.indexes  ?? 822;

  const pgTables = pgSchema?.tables ?? 14;
  const pgViews  = pgSchema?.views  ?? 3;

  const oracleConn = health?.oracle    !== false;
  const pgConn     = health?.postgres  !== false;

  const openEditor = () => openTab({ id: 'ddl-editor', title: 'DDL Editor', type: 'editor' });
  const openGrid   = () => openTab({ id: 'data-preview', title: 'Data Preview', type: 'grid' });
  const openGen    = () => navigate('/generator');

  return (
    <div style={{
      width: 'var(--sidebar-w)', height: '100%',
      background: 'var(--color-panel)',
      borderRight: '1px solid var(--color-border)',
      display: 'flex', flexDirection: 'column',
      overflow: 'hidden', flexShrink: 0,
    }}>
      {/* Header */}
      <div className="ide-section-header" style={{ flexShrink: 0 }}>Explorer</div>

      {/* Tree */}
      <div style={{ flex: 1, overflowY: 'auto', overflowX: 'hidden' }}>

        {/* ── Quick Nav ── */}
        {hasScreen('dashboard') && (
          <TreeItem label="Dashboard" icon={LayoutGrid} onClick={() => openTab({ id: 'dashboard', title: 'Dashboard', type: 'dashboard' })} />
        )}

        {/* ── Oracle Source ── */}
        <SectionHeader label="Oracle (Source)" />
        <TreeItem label="Oracle Database" icon={Database} dot={oracleConn ? 'green' : 'red'} defaultOpen={true} depth={0}
                  badge={oracleConn ? 'Connected' : 'Disconnected'}>
          {hasScreen('sql_editor') && (
            <TreeItem label="Tables" icon={Table2} depth={1} badge={oracleTables} defaultOpen={false}>
              <TreeItem label="provider"  depth={2} onClick={openEditor} />
              <TreeItem label="common"    depth={2} onClick={openEditor} />
              <TreeItem label="public"    depth={2} onClick={openEditor} />
            </TreeItem>
          )}
          <TreeItem label="Views"    icon={LayoutGrid} depth={1} badge={oracleViews}   />
          <TreeItem label="Indexes"  icon={ListTree}   depth={1} badge={oracleIndexes} />
          <TreeItem label="Packages" icon={FileText}   depth={1} badge={oraclePkgs}    />
        </TreeItem>

        {/* ── PostgreSQL Target ── */}
        <SectionHeader label="PostgreSQL (Target)" />
        <TreeItem label="PostgreSQL" icon={Database} dot={pgConn ? 'green' : 'red'} depth={0}
                  badge={pgConn ? 'Connected' : 'Disconnected'}>
          {hasScreen('data_preview') && (
            <TreeItem label="Tables" icon={Table2} depth={1} badge={pgTables} onClick={openGrid} />
          )}
          <TreeItem label="Views" icon={LayoutGrid} depth={1} badge={pgViews} />
        </TreeItem>

        {/* ── Tools ── */}
        <SectionHeader label="Tools" />
        {can('execute_dml') && (
          <TreeItem label="Smart Test Data Generator" icon={CheckSquare} onClick={openGen} />
        )}
        <TreeItem label="Dependency Explorer"  icon={ListTree}   />
        <TreeItem label="Conversion Rules"     icon={FileText}   />
        <TreeItem label="Migration Tasks"      icon={CheckSquare}/>
        {hasScreen('validation') && <TreeItem label="Validation" icon={AlertCircle} />}
        {hasScreen('reports')    && <TreeItem label="Reports"    icon={FileText}    />}
        {hasScreen('logs')       && <TreeItem label="Execution History" icon={History} />}
        {can('manage_users')     && <TreeItem label="User Management"   icon={Settings} />}
        {can('manage_settings')  && <TreeItem label="Settings"          icon={Settings} />}
      </div>
    </div>
  );
}
