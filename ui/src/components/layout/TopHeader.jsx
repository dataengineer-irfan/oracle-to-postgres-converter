import React from 'react';
import { Database, Search, Bell, Settings, ChevronDown, ArrowRight, Shield, LogOut } from 'lucide-react';
import { useStore } from '../../store/useStore';
import { useNavigate } from 'react-router-dom';
import { ROLE_COLORS, ROLE_LABELS } from '../../rbac/roles';

export default function TopHeader() {
  const user = useStore(state => state.user);
  const logout = useStore(state => state.logout);
  const navigate = useNavigate();

  const roleBg   = ROLE_COLORS[user?.role]?.bg   ?? 'rgba(37,99,235,0.15)';
  const roleText = ROLE_COLORS[user?.role]?.text  ?? '#2563EB';
  const roleLabel= ROLE_LABELS[user?.role]        ?? 'User';

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header
      className="bg-panel ide-border-b flex items-center justify-between px-3 select-none shrink-0"
      style={{ height: 'var(--header-h)' }}
    >
      {/* Left: App identity */}
      <div className="flex items-center gap-2 shrink-0">
        <Database className="text-primary" style={{ width: 16, height: 16 }} />
        <span className="text-sm font-semibold text-text whitespace-nowrap">ETS Migration Studio</span>
        <span className="text-xs text-muted hidden md:inline">—</span>
        <span className="text-xs text-muted hidden md:inline whitespace-nowrap">Enterprise DB Modernization</span>
      </div>

      {/* Center: Context ribbon */}
      <div className="flex items-center gap-0 text-xs text-muted overflow-hidden mx-4 flex-1 min-w-0">
        {[
          { label: 'Project',     value: 'Oracle-Financials' },
          { label: 'Workspace',   value: 'Alpha-Team' },
          { label: 'Branch',      value: 'feature/hr' },
          { label: 'Env',         value: 'Staging', valueClass: 'text-success' },
        ].map((item, i) => (
          <React.Fragment key={item.label}>
            {i > 0 && <span className="text-border mx-2">|</span>}
            <button className="flex items-center gap-1 btn-ghost px-1 h-full whitespace-nowrap" style={{ height: 'var(--header-h)', fontSize: 12 }}>
              <span className="text-muted">{item.label}:</span>
              <span className={item.valueClass ?? 'text-text'}>{item.value}</span>
              <ChevronDown style={{ width: 10, height: 10 }} className="text-muted" />
            </button>
          </React.Fragment>
        ))}

        <span className="text-border mx-2">|</span>

        {/* DB Version indicator */}
        <div className="flex items-center gap-1 text-xs whitespace-nowrap">
          <span className="text-warning font-medium">Oracle 19c</span>
          <ArrowRight style={{ width: 10, height: 10 }} className="text-muted" />
          <span className="text-primary font-medium">PostgreSQL 17</span>
        </div>
      </div>

      {/* Right: Search + actions + user */}
      <div className="flex items-center gap-2 shrink-0">
        {/* Search */}
        <div className="relative hidden lg:flex items-center">
          <Search className="absolute left-2 text-muted" style={{ width: 12, height: 12 }} />
          <input
            type="text"
            placeholder="Search… (Ctrl+K)"
            className="bg-bg ide-border text-text placeholder:text-muted focus:outline-none focus:border-primary"
            style={{ height: 24, paddingLeft: 24, paddingRight: 8, width: 200, fontSize: 12, borderRadius: 'var(--radius)' }}
          />
        </div>

        {/* Notifications */}
        <div className="relative group">
          <button className="btn-ghost relative" style={{ width: 28, height: 28, padding: 0 }}>
            <Bell style={{ width: 14, height: 14 }} />
            <span className="absolute top-1 right-1 w-1.5 h-1.5 bg-error rounded-full"></span>
          </button>
          {/* Dropdown */}
          <div className="absolute right-0 top-full mt-1 w-56 bg-panel ide-border hidden group-hover:block z-50"
               style={{ boxShadow: 'var(--shadow-dropdown, 0 4px 16px rgba(0,0,0,0.5))' }}>
            <div className="ide-section-header" style={{ border: 'none', borderBottom: '1px solid var(--color-border)' }}>Notifications</div>
            {[
              { msg: 'Conversion complete: hr_schema', color: 'var(--color-success)' },
              { msg: 'Validation failed: CUSTOMER_SEQ', color: 'var(--color-error)' },
              { msg: 'Dependency changed: DEPT_VIEW', color: 'var(--color-warning)' },
            ].map((n, i) => (
              <div key={i} className="flex items-center gap-2 px-2 py-1.5 hover:bg-border cursor-pointer"
                   style={{ fontSize: 12, borderLeft: `2px solid ${n.color}` }}>
                <span className="text-text">{n.msg}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Settings — admin only */}
        {user?.role === 'admin' && (
          <button className="btn-ghost" style={{ width: 28, height: 28, padding: 0 }}>
            <Settings style={{ width: 14, height: 14 }} />
          </button>
        )}

        {/* Separator */}
        <div className="ide-border-l" style={{ height: 20, margin: '0 4px' }}></div>

        {/* Role badge + user */}
        <div className="flex items-center gap-2">
          <span className="role-badge" style={{ background: roleBg, color: roleText }}>
            {roleLabel}
          </span>
          <span className="text-xs text-text whitespace-nowrap">{user?.name ?? 'User'}</span>
          <button className="btn-ghost" style={{ width: 24, height: 24, padding: 0 }} onClick={handleLogout} title="Sign out">
            <LogOut style={{ width: 12, height: 12 }} />
          </button>
        </div>
      </div>
    </header>
  );
}
