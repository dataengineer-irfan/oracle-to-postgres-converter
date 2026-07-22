import React from 'react';
import { Lock, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { usePermissions } from '../rbac/usePermissions';
import { ROLE_LABELS, ROLE_COLORS } from '../rbac/roles';

export default function Unauthorized() {
  const navigate = useNavigate();
  const { role } = usePermissions();
  const roleColor = ROLE_COLORS[role];

  return (
    <div style={{
      height: '100vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'var(--color-bg)', color: 'var(--color-text)',
      fontFamily: 'Inter, sans-serif', gap: 16,
    }}>
      <Lock style={{ width: 32, height: 32, color: 'var(--color-muted)' }} />
      <div style={{ fontSize: 18, fontWeight: 600 }}>Access Restricted</div>
      <div style={{ fontSize: 13, color: 'var(--color-muted)', textAlign: 'center', maxWidth: 320 }}>
        Your role&nbsp;
        <span className="role-badge" style={{ background: roleColor?.bg, color: roleColor?.text, fontSize: 11 }}>
          {ROLE_LABELS[role]}
        </span>
        &nbsp;does not have permission to access this page.
      </div>
      <button className="btn-secondary" style={{ marginTop: 8, display: 'flex', alignItems: 'center', gap: 6 }}
              onClick={() => navigate('/ide')}>
        <ArrowLeft style={{ width: 14, height: 14 }} />
        Back to workspace
      </button>
    </div>
  );
}
