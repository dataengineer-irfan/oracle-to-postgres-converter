import React from 'react';
import { Lock } from 'lucide-react';
import { usePermissions } from './usePermissions';
import { ROLE_LABELS } from './roles';

/**
 * PermissionGate
 * Wraps any content and shows a lock overlay if the user lacks permission.
 * 
 * Props:
 *   permission — string: a key from PERMISSIONS
 *   screen     — string: a key from SCREEN_PERMISSIONS (alternative to permission)
 *   overlay    — bool (default true): show lock overlay instead of hiding entirely
 *   fallback   — JSX: custom content to show instead of the lock overlay
 */
export default function PermissionGate({ permission, screen, overlay = true, fallback, children }) {
  const { can, hasScreen, role } = usePermissions();

  const allowed = permission ? can(permission) : screen ? hasScreen(screen) : true;

  if (allowed) return <>{children}</>;

  if (fallback) return <>{fallback}</>;

  if (!overlay) return null;

  return (
    <div className="relative w-full h-full">
      {/* Blurred content underneath */}
      <div style={{ opacity: 0.15, pointerEvents: 'none', filter: 'blur(2px)', width: '100%', height: '100%' }}>
        {children}
      </div>
      {/* Lock overlay */}
      <div className="permission-lock">
        <Lock style={{ width: 24, height: 24, color: 'var(--color-muted)', marginBottom: 8 }} />
        <div style={{ fontSize: 13, color: 'var(--color-text)', fontWeight: 600, marginBottom: 4 }}>
          Access Restricted
        </div>
        <div style={{ fontSize: 12, color: 'var(--color-muted)', textAlign: 'center', maxWidth: 240 }}>
          Your role <strong style={{ color: 'var(--color-text)' }}>{ROLE_LABELS[role]}</strong> does not have
          permission to access this area.
        </div>
      </div>
    </div>
  );
}
