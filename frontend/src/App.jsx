import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useStore } from './store/useStore';
import Login        from './pages/Login';
import IDE          from './pages/IDE';
import DataGenerator from './pages/DataGenerator';
import Unauthorized  from './pages/Unauthorized';
import { usePermissions } from './rbac/usePermissions';

// ── Route guards ──────────────────────────────────────────────────────────────

function RequireAuth({ children }) {
  const user = useStore(state => state.user);
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function RequireScreen({ screen, children }) {
  // Must be inside RequireAuth, so user exists
  const { hasScreen, role } = usePermissions();
  if (!hasScreen(screen)) {
    // QA users always go to their dedicated page
    if (role === 'qa') return <Navigate to="/generator" replace />;
    return <Navigate to="/unauthorized" replace />;
  }
  return children;
}

// ── App ───────────────────────────────────────────────────────────────────────

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Public */}
        <Route path="/login"        element={<Login />} />
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* Protected */}
        <Route path="/ide" element={
          <RequireAuth>
            <RequireScreen screen="dashboard">
              <IDE />
            </RequireScreen>
          </RequireAuth>
        } />

        <Route path="/generator" element={
          <RequireAuth>
            <RequireScreen screen="data_generator">
              <DataGenerator />
            </RequireScreen>
          </RequireAuth>
        } />

        {/* Default */}
        <Route path="*" element={<Navigate to="/ide" replace />} />
      </Routes>
    </Router>
  );
}
