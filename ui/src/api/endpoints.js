/**
 * All API endpoints — never hardcode URLs in components.
 * Change base URL here to switch environments.
 */

// Use VITE_API_URL if provided (e.g. on Render), fallback to relative path (if served together) or localhost
export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// Construct WebSocket URL by replacing http with ws
export const WS_BASE = API_BASE.replace(/^http/, 'ws');

export const ENDPOINTS = {
  // Auth
  LOGIN:               `${API_BASE}/auth/login`,

  // Migration status
  MIGRATION_STATUS:    `${API_BASE}/api/migration/status`,
  MIGRATION_STATS:     `${API_BASE}/api/migration/stats`,
  PROJECTS:            `${API_BASE}/api/projects`,

  // Schema
  SCHEMA_ORACLE:       `${API_BASE}/api/schema/oracle`,
  SCHEMA_POSTGRES:     `${API_BASE}/api/schema/postgres`,

  // Connections
  CONNECTIONS_HEALTH:  `${API_BASE}/api/connections/health`,

  // AI
  AI_ANALYSIS:         `${API_BASE}/api/ai/analysis`,
  PARSE_INTENT:        `${API_BASE}/parse-intent`,

  // Data
  DATA_TABLE:          (table) => `${API_BASE}/api/data/${table}`,
  PREVIEW_DML:         `${API_BASE}/api/data/preview-dml`,
  SQL_EXECUTE:         `${API_BASE}/api/sql/execute`,
  EXECUTE_PIPELINE:    `${API_BASE}/execute`,

  // Validation
  VALIDATION_RESULTS:  `${API_BASE}/api/validation/results`,

  // WebSocket
  WS_LOGS:             `${WS_BASE}/ws/logs`,
};
