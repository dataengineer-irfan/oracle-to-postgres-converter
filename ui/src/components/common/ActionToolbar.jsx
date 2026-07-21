import React, { useState } from 'react';
import { Copy, Download, Search, Share2, Printer, Maximize2, Loader2, Filter } from 'lucide-react';

/**
 * Universal ActionToolbar — locked spec, never deviates.
 * Order: Copy | Download | separator | Search | Filter | separator | Clear | separator | Share | Print | Fullscreen
 * 
 * Props:
 *   title     — string shown at left
 *   type      — badge label (LOG, SQL, DML, etc.)
 *   loading   — shows spinner on Copy/Download while API in flight
 *   onCopy    — (format: string) => void
 *   onDownload— (format: string) => void
 *   onSearch  — () => void
 *   onFilter  — () => void
 *   onClear   — () => void
 *   onShare   — () => void
 *   onPrint   — () => void
 *   onFullscreen — () => void
 *   extra     — JSX for context-specific tools (e.g. Run, Validate for SQL editor)
 *               rendered BEFORE the separator
 */

function TBtn({ icon: Icon, label, onClick, active, loading: isLoading, title: tip, children }) {
  return (
    <button
      className={`btn-ghost flex items-center gap-1 ${!onClick ? 'opacity-40 cursor-not-allowed' : ''}`}
      style={{ height: 28, padding: '0 6px', fontSize: 12 }}
      onClick={onClick}
      disabled={!onClick}
      title={tip ?? label}
    >
      {isLoading
        ? <span className="ide-spinner" />
        : <Icon style={{ width: 14, height: 14 }} />
      }
      {label && <span>{label}</span>}
      {children}
    </button>
  );
}

function Sep() {
  return <div style={{ width: 1, height: 16, background: 'var(--color-border)', margin: '0 4px', flexShrink: 0 }} />;
}

function CopyMenu({ loading, onCopy }) {
  const [open, setOpen] = useState(false);
  const formats = [
    { label: 'Copy All',      value: 'all' },
    { label: 'Copy Selected', value: 'selected' },
    { label: 'Copy as SQL',   value: 'sql' },
    { label: 'Copy as DDL',   value: 'ddl' },
    { label: 'Copy as DML',   value: 'dml' },
    { label: 'Copy as JSON',  value: 'json' },
    { label: 'Copy as CSV',   value: 'csv' },
  ];
  return (
    <div className="relative">
      <TBtn icon={Copy} label="Copy" loading={loading} onClick={onCopy ? () => setOpen(o => !o) : undefined} />
      {open && (
        <div className="absolute top-full left-0 mt-0.5 bg-panel ide-border z-50"
             style={{ minWidth: 140, boxShadow: '0 4px 16px rgba(0,0,0,0.5)' }}>
          {formats.map(f => (
            <button key={f.value}
              className="flex w-full items-center px-3 text-muted hover:text-text hover:bg-border"
              style={{ height: 28, fontSize: 12 }}
              onClick={() => { onCopy?.(f.value); setOpen(false); }}>
              {f.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function DownloadMenu({ loading, onDownload }) {
  const [open, setOpen] = useState(false);
  const formats = [
    { label: 'SQL File (.sql)',    value: 'sql' },
    { label: 'Text File (.txt)',   value: 'txt' },
    { label: 'CSV File (.csv)',    value: 'csv' },
    { label: 'JSON File (.json)',  value: 'json' },
    { label: 'HTML Report (.html)',value: 'html' },
    { label: 'PDF Report (.pdf)',  value: 'pdf' },
    { label: 'Archive (.zip)',     value: 'zip' },
  ];
  return (
    <div className="relative">
      <TBtn icon={Download} label="Download" loading={loading} onClick={onDownload ? () => setOpen(o => !o) : undefined} />
      {open && (
        <div className="absolute top-full left-0 mt-0.5 bg-panel ide-border z-50"
             style={{ minWidth: 160, boxShadow: '0 4px 16px rgba(0,0,0,0.5)' }}>
          {formats.map(f => (
            <button key={f.value}
              className="flex w-full items-center px-3 text-muted hover:text-text hover:bg-border"
              style={{ height: 28, fontSize: 12 }}
              onClick={() => { onDownload?.(f.value); setOpen(false); }}>
              {f.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ActionToolbar({
  title, type,
  loading = false,
  onCopy, onDownload,
  onSearch, onFilter,
  onClear, onShare, onPrint, onFullscreen,
  extra,
}) {
  return (
    <div className="ide-toolbar ide-border-b" style={{ justifyContent: 'space-between' }}>
      {/* Left: label */}
      <div className="flex items-center gap-2">
        {type && (
          <span style={{
            fontSize: 10, fontWeight: 600, letterSpacing: '0.08em',
            padding: '1px 6px', borderRadius: 'var(--radius)',
            background: 'rgba(37,99,235,0.12)', color: 'var(--color-primary)',
            textTransform: 'uppercase',
          }}>
            {type}
          </span>
        )}
        {title && <span style={{ fontSize: 13, color: 'var(--color-text)' }}>{title}</span>}
        {loading && <span className="ide-spinner" />}
      </div>

      {/* Right: tools — LOCKED ORDER */}
      <div className="flex items-center">
        {/* Context-specific (e.g. Run, Validate) */}
        {extra && <>{extra}<Sep /></>}

        {/* Copy */}
        <CopyMenu loading={loading} onCopy={onCopy} />

        {/* Download */}
        <DownloadMenu loading={loading} onDownload={onDownload} />

        <Sep />

        {/* Search */}
        <TBtn icon={Search} onClick={onSearch} tip="Search" />
        {/* Filter */}
        <TBtn icon={Filter} onClick={onFilter} tip="Filter" />

        <Sep />

        {/* Share */}
        <TBtn icon={Share2} onClick={onShare} tip="Share" />
        {/* Print */}
        <TBtn icon={Printer} onClick={onPrint} tip="Print" />
        {/* Fullscreen */}
        <TBtn icon={Maximize2} onClick={onFullscreen} tip="Fullscreen" />
      </div>
    </div>
  );
}
