import React, { useState } from 'react';
import { ChevronRight, ChevronDown, Database, Table2, LayoutGrid, Settings, History, AlertCircle, FileText, CheckSquare, ListTree } from 'lucide-react';
import { useStore } from '../../store/useStore';
import { useNavigate } from 'react-router-dom';
import { usePermissions } from '../../rbac/usePermissions';
import { useLiveData } from '../../hooks/useLiveData';
import { ENDPOINTS } from '../../api/endpoints';

// ── Tree Item ─────────────────────────────────────────────────────────────────
function TreeItem({ id, label, depth = 0, icon: Icon, children, defaultOpen = false, onClick, badge, dot }) {
  const [open, setOpen] = useState(() => {
    if (!id) return defaultOpen;
    const saved = localStorage.getItem(`tree_${id}`);
    return saved !== null ? saved === 'true' : defaultOpen;
  });

  const toggle = () => {
    setOpen(o => {
      const next = !o;
      if (id) localStorage.setItem(`tree_${id}`, next);
      return next;
    });
  };

  const hasChildren = !!children;

  return (
    <div>
      <div
        className="ide-tree-item"
        style={{ paddingLeft: 8 + depth * 20 }}
        onClick={() => { if (hasChildren) toggle(); if (onClick) onClick(); }}
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
function ExpandableSection({ id, label, children, defaultOpen = true }) {
  const [open, setOpen] = useState(() => {
    if (!id) return defaultOpen;
    const saved = localStorage.getItem(`section_${id}`);
    return saved !== null ? saved === 'true' : defaultOpen;
  });

  const toggle = () => {
    setOpen(o => {
      const next = !o;
      if (id) localStorage.setItem(`section_${id}`, next);
      return next;
    });
  };

  return (
    <div>
      <div style={{
        height: 24, display: 'flex', alignItems: 'center',
        padding: '0 8px', fontSize: 11, fontWeight: 600,
        color: 'var(--color-muted)', textTransform: 'uppercase',
        letterSpacing: '0.08em', borderTop: '1px solid var(--color-border)',
        marginTop: 4, cursor: 'pointer', userSelect: 'none'
      }} onClick={toggle} className="hover:text-text transition-colors">
        <span style={{ width: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          {open ? <ChevronDown style={{ width: 12, height: 12 }} /> : <ChevronRight style={{ width: 12, height: 12 }} />}
        </span>
        {label}
      </div>
      {open && <div>{children}</div>}
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

  const oracleTables  = oracleSchema?.tables  ?? 0;
  const oracleViews   = oracleSchema?.views   ?? 0;
  const oraclePkgs    = oracleSchema?.packages ?? 0;
  const oracleIndexes = oracleSchema?.indexes  ?? 0;

  const pgTables = pgSchema?.tables ?? 0;
  const pgViews  = pgSchema?.views  ?? 0;

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
          <TreeItem id="nav_dashboard" label="Dashboard" icon={LayoutGrid} onClick={() => openTab({ id: 'dashboard', title: 'Dashboard', type: 'dashboard' })} />
        )}

        {/* ── Oracle Source ── */}
        <ExpandableSection id="sec_oracle" label="Oracle (Source)" defaultOpen={true}>
          <TreeItem id="tree_oracle_db" label="Oracle Database" icon={Database} dot={oracleConn ? 'green' : 'red'} defaultOpen={true} depth={0}
                    badge={oracleConn ? 'Connected' : 'Disconnected'}>
            {hasScreen('sql_editor') && (
              <TreeItem id="tree_oracle_tables" label="Tables" icon={Table2} depth={1} badge={oracleTables} defaultOpen={false}>
                <TreeItem id="tree_oracle_tbl_provider" label="provider"  depth={2} onClick={openEditor} />
                <TreeItem id="tree_oracle_tbl_common" label="common"    depth={2} onClick={openEditor} />
                <TreeItem id="tree_oracle_tbl_public" label="public"    depth={2} onClick={openEditor} />
              </TreeItem>
            )}
            <TreeItem id="tree_oracle_views" label="Views"    icon={LayoutGrid} depth={1} badge={oracleViews}   />
            <TreeItem id="tree_oracle_indexes" label="Indexes"  icon={ListTree}   depth={1} badge={oracleIndexes} />
            <TreeItem id="tree_oracle_packages" label="Packages" icon={FileText}   depth={1} badge={oraclePkgs}    />
          </TreeItem>
        </ExpandableSection>

        {/* ── PostgreSQL Target ── */}
        <ExpandableSection id="sec_postgres" label="PostgreSQL (Target)" defaultOpen={true}>
          <TreeItem id="tree_pg_db" label="PostgreSQL" icon={Database} dot={pgConn ? 'green' : 'red'} depth={0} defaultOpen={true}
                    badge={pgConn ? 'Connected' : 'Disconnected'}>
            {hasScreen('data_preview') && (
              <TreeItem id="tree_pg_tables" label="Tables" icon={Table2} depth={1} badge={pgTables} onClick={openGrid} />
            )}
            <TreeItem id="tree_pg_views" label="Views" icon={LayoutGrid} depth={1} badge={pgViews} />
          </TreeItem>
        </ExpandableSection>

        {/* ── Tools ── */}
        <ExpandableSection id="sec_tools" label="Tools" defaultOpen={true}>
          {can('execute_dml') && (
            <TreeItem id="tree_tools_gen" label="Smart Test Data Generator" icon={CheckSquare} onClick={openGen} />
          )}
          <TreeItem id="tree_tools_deps" label="Dependency Explorer"  icon={ListTree}   />
          <TreeItem id="tree_tools_rules" label="Conversion Rules"     icon={FileText}   />
          <TreeItem id="tree_tools_tasks" label="Migration Tasks"      icon={CheckSquare}/>
          {hasScreen('validation') && <TreeItem id="tree_tools_valid" label="Validation" icon={AlertCircle} />}
          {hasScreen('reports')    && <TreeItem id="tree_tools_reports" label="Reports"    icon={FileText}    />}
          {hasScreen('logs')       && <TreeItem id="tree_tools_logs" label="Execution History" icon={History} />}
          {can('manage_users')     && <TreeItem id="tree_tools_users" label="User Management"   icon={Settings} />}
          {can('manage_settings')  && <TreeItem id="tree_tools_settings" label="Settings"          icon={Settings} />}
        </ExpandableSection>
      </div>
    </div>
  );
}
