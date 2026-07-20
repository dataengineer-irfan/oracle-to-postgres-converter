import React, { useState } from 'react';
import { Database, CheckCircle, Shield, ChevronDown } from 'lucide-react';
import { useStore } from '../store/useStore';
import { ROLE_LABELS, ROLE_COLORS } from '../rbac/roles';
import { useNavigate } from 'react-router-dom';

const DEMO_USERS = [
  { role: 'admin',    name: 'Admin User',        email: 'admin@ets.com',    password: 'Admin@2026' },
  { role: 'engineer', name: 'Migration Engineer', email: 'engineer@ets.com', password: 'Eng@2026'   },
  { role: 'qa',       name: 'QA Engineer',        email: 'qa@ets.com',       password: 'QA@2026'    },
  { role: 'analyst',  name: 'Data Analyst',       email: 'analyst@ets.com',  password: 'Analyst@2026'},
  { role: 'auditor',  name: 'Compliance Auditor', email: 'auditor@ets.com',  password: 'Audit@2026' },
];

export default function Login() {
  const login = useStore(state => state.login);
  const navigate = useNavigate();
  const [selectedRole, setSelectedRole] = useState('engineer');
  const [email, setEmail]               = useState('');
  const [password, setPassword]         = useState('');
  const [error, setError]               = useState('');
  const [roleOpen, setRoleOpen]         = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // Match by email AND password
    const matched = DEMO_USERS.find(
      u => u.email === email.trim() && u.password === password
    );

    if (matched) {
      setSelectedRole(matched.role);
      login({ name: matched.name, email: matched.email, role: matched.role });
      // QA goes directly to the Data Generator — their only page
      navigate(matched.role === 'qa' ? '/generator' : '/ide');
    } else {
      setError('Invalid email or password.');
    }
  };

  const roleColor = ROLE_COLORS[selectedRole];

  return (
    <div style={{ display: 'flex', height: '100vh', background: 'var(--color-bg)', color: 'var(--color-text)', fontFamily: 'Inter, sans-serif' }}>

      {/* Left panel — product info */}
      <div style={{
        width: '55%', background: 'var(--color-panel)',
        borderRight: '1px solid var(--color-border)',
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
        padding: 48, position: 'relative', overflow: 'hidden',
      }} className="hidden lg:flex">
        {/* Subtle grid background */}
        <div style={{
          position: 'absolute', inset: 0, opacity: 0.03,
          backgroundImage: 'linear-gradient(var(--color-border) 1px, transparent 1px), linear-gradient(90deg, var(--color-border) 1px, transparent 1px)',
          backgroundSize: '24px 24px',
        }} />

        <div style={{ position: 'relative', zIndex: 1 }}>
          {/* Brand */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 48 }}>
            <div style={{
              width: 36, height: 36, background: 'var(--color-primary)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <Database style={{ width: 18, height: 18, color: '#fff' }} />
            </div>
            <div>
              <div style={{ fontSize: 16, fontWeight: 700 }}>ETS Migration Studio</div>
              <div style={{ fontSize: 12, color: 'var(--color-muted)' }}>Enterprise Database Modernization</div>
            </div>
          </div>

          {/* Features */}
          <div style={{ fontSize: 24, fontWeight: 700, marginBottom: 32, lineHeight: '32px' }}>
            Oracle → PostgreSQL<br />
            <span style={{ color: 'var(--color-primary)' }}>Migration Platform</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {[
              'AI-powered schema conversion & DDL generation',
              'Oracle compatibility analysis & dependency mapping',
              'Automated data type mapping & validation',
              'Smart test data generation (DML pipeline)',
              'Real-time execution logs & migration reports',
              'Role-based access control (5 roles)',
            ].map((f, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 13, color: 'var(--color-muted)' }}>
                <CheckCircle style={{ width: 14, height: 14, color: 'var(--color-success)', flexShrink: 0 }} />
                {f}
              </div>
            ))}
          </div>
        </div>

        <div style={{ position: 'relative', zIndex: 1, display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: 12, color: 'var(--color-muted)' }}>
          <span>v2.4.0 Enterprise Edition</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <Shield style={{ width: 12, height: 12 }} />
            SOC2 Certified
          </div>
        </div>
      </div>

      {/* Right panel — login form */}
      <div style={{
        flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: 32,
      }}>
        <div style={{ width: '100%', maxWidth: 360 }}>
          <div style={{ marginBottom: 32 }}>
            <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 4 }}>Sign in to workspace</div>
            <div style={{ fontSize: 13, color: 'var(--color-muted)' }}>Enter your credentials to continue</div>
          </div>

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {/* Role Selector */}
            <div>
              <label style={{ display: 'block', fontSize: 12, color: 'var(--color-muted)', marginBottom: 4, fontWeight: 500 }}>
                Role (Demo)
              </label>
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setRoleOpen(o => !o)}
                  style={{
                    width: '100%', height: 32, padding: '0 10px',
                    background: 'var(--color-bg)', border: '1px solid var(--color-border)',
                    borderRadius: 'var(--radius)', color: 'var(--color-text)',
                    fontSize: 13, display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    cursor: 'pointer',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span className="role-badge" style={{ background: roleColor?.bg, color: roleColor?.text }}>
                      {ROLE_LABELS[selectedRole]}
                    </span>
                    <span style={{ fontSize: 12, color: 'var(--color-muted)' }}>
                      {DEMO_USERS.find(u => u.role === selectedRole)?.name}
                    </span>
                  </div>
                  <ChevronDown style={{ width: 12, height: 12, color: 'var(--color-muted)' }} />
                </button>
                {roleOpen && (
                  <div style={{
                    position: 'absolute', top: '100%', left: 0, right: 0,
                    background: 'var(--color-panel)', border: '1px solid var(--color-border)',
                    zIndex: 50, boxShadow: '0 4px 16px rgba(0,0,0,0.5)',
                  }}>
                    {DEMO_USERS.map(u => {
                      const rc = ROLE_COLORS[u.role];
                      return (
                        <button
                          key={u.role} type="button"
                          onClick={() => { setSelectedRole(u.role); setRoleOpen(false); }}
                          style={{
                            width: '100%', height: 36, padding: '0 10px',
                            display: 'flex', alignItems: 'center', gap: 10,
                            background: selectedRole === u.role ? 'rgba(37,99,235,0.1)' : 'transparent',
                            border: 'none', color: 'var(--color-text)', cursor: 'pointer',
                            fontSize: 13, textAlign: 'left',
                            borderBottom: '1px solid var(--color-border)',
                          }}
                        >
                          <span className="role-badge" style={{ background: rc?.bg, color: rc?.text }}>
                            {ROLE_LABELS[u.role]}
                          </span>
                          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                            <span>{u.name}</span>
                            <span style={{ fontSize: 11, color: 'var(--color-muted)' }}>{u.email}</span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>

            {/* Email */}
            <div>
              <label style={{ display: 'block', fontSize: 12, color: 'var(--color-muted)', marginBottom: 4, fontWeight: 500 }}>
                Email
              </label>
              <input
                type="email" value={email} onChange={e => setEmail(e.target.value)}
                placeholder={DEMO_USERS.find(u => u.role === selectedRole)?.email}
                style={{
                  width: '100%', height: 32, padding: '0 10px',
                  background: 'var(--color-bg)', border: '1px solid var(--color-border)',
                  borderRadius: 'var(--radius)', color: 'var(--color-text)',
                  fontSize: 13, outline: 'none',
                }}
                onFocus={e => e.target.style.borderColor = 'var(--color-primary)'}
                onBlur={e  => e.target.style.borderColor = 'var(--color-border)'}
              />
            </div>

            {/* Password */}
            <div>
              <label style={{ display: 'block', fontSize: 12, color: 'var(--color-muted)', marginBottom: 4, fontWeight: 500 }}>
                Password
              </label>
              <input
                type="password" value={password} onChange={e => setPassword(e.target.value)}
                placeholder="Any password for demo"
                style={{
                  width: '100%', height: 32, padding: '0 10px',
                  background: 'var(--color-bg)', border: '1px solid var(--color-border)',
                  borderRadius: 'var(--radius)', color: 'var(--color-text)',
                  fontSize: 13, outline: 'none',
                }}
                onFocus={e => e.target.style.borderColor = 'var(--color-primary)'}
                onBlur={e  => e.target.style.borderColor = 'var(--color-border)'}
              />
            </div>

            {error && (
              <div style={{ fontSize: 12, color: 'var(--color-error)', padding: '6px 8px', background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: 'var(--radius)' }}>
                {error}
              </div>
            )}

            <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: 8, height: 36, fontSize: 13 }}>
              Sign in to workspace
            </button>
          </form>

          {/* SSO */}
          <div style={{ marginTop: 24 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
              <div style={{ flex: 1, height: 1, background: 'var(--color-border)' }} />
              <span style={{ fontSize: 12, color: 'var(--color-muted)' }}>or continue with SSO</span>
              <div style={{ flex: 1, height: 1, background: 'var(--color-border)' }} />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8 }}>
              {['Azure AD', 'Okta', 'Google'].map(p => (
                <button key={p} className="btn-secondary" style={{ height: 32, fontSize: 12 }}>{p}</button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
