import { useStore } from '../store/useStore';
import { PERMISSIONS, SCREEN_PERMISSIONS } from './roles';

/**
 * usePermissions hook
 * Returns:
 *   can(permission)  — boolean: does current user have this permission?
 *   hasScreen(screen)— boolean: can current user view this screen?
 *   role             — current role string
 */
export function usePermissions() {
  const user = useStore(state => state.user);
  const role = user?.role ?? 'auditor'; // safest default

  const can = (permission) => {
    const allowed = PERMISSIONS[permission];
    if (!allowed) return false;
    return allowed.includes(role);
  };

  const hasScreen = (screen) => {
    const permission = SCREEN_PERMISSIONS[screen];
    if (!permission) return true; // no restriction = open
    return can(permission);
  };

  return { can, hasScreen, role };
}
