/**
 * RBAC Role Definitions
 * 5 roles: admin | engineer | qa | analyst | auditor
 */

export const ROLES = {
  ADMIN:    'admin',
  ENGINEER: 'engineer',
  QA:       'qa',
  ANALYST:  'analyst',
  AUDITOR:  'auditor',
};

export const ROLE_LABELS = {
  admin:    'Admin',
  engineer: 'Engineer',
  qa:       'QA',
  analyst:  'Analyst',
  auditor:  'Auditor',
};

export const ROLE_COLORS = {
  admin:    { bg: 'rgba(239,68,68,0.12)',   text: '#EF4444' },
  engineer: { bg: 'rgba(37,99,235,0.12)',   text: '#2563EB' },
  qa:       { bg: 'rgba(245,158,11,0.12)',  text: '#F59E0B' },
  analyst:  { bg: 'rgba(34,197,94,0.12)',   text: '#22C55E' },
  auditor:  { bg: 'rgba(148,163,184,0.12)', text: '#94A3B8' },
};

/**
 * Permission Matrix
 * key: permission name
 * value: set of roles that have it
 */
export const PERMISSIONS = {
  // Screens
  view_dashboard:     ['admin', 'engineer', 'analyst'],
  view_sql_editor:    ['admin', 'engineer'],
  view_data_generator:['admin', 'engineer', 'qa'],
  view_data_preview:  ['admin', 'engineer', 'analyst'],
  view_schema:        ['admin', 'engineer', 'analyst'],
  view_ai_panel:      ['admin', 'engineer', 'analyst'],
  view_validation:    ['admin', 'engineer', 'analyst', 'auditor'],
  view_logs:          ['admin', 'engineer', 'auditor'],
  view_reports:       ['admin', 'engineer', 'analyst', 'auditor'],
  view_ai_sql_assistant: ['admin', 'engineer', 'qa', 'analyst', 'auditor'],

  // Actions
  execute_dml:        ['admin', 'engineer', 'qa'],
  execute_migration:  ['admin', 'engineer'],
  download_output:    ['admin', 'engineer', 'qa', 'analyst', 'auditor'],
  copy_output:        ['admin', 'engineer', 'qa', 'analyst', 'auditor'],
  manage_users:       ['admin'],
  manage_settings:    ['admin'],
};

/**
 * Screen route → permission mapping
 */
export const SCREEN_PERMISSIONS = {
  dashboard:      'view_dashboard',
  sql_editor:     'view_sql_editor',
  data_generator: 'view_data_generator',
  data_preview:   'view_data_preview',
  schema:         'view_schema',
  ai_panel:       'view_ai_panel',
  validation:     'view_validation',
  logs:           'view_logs',
  reports:        'view_reports',
};
