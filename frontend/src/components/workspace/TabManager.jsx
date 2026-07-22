import React from 'react';
import { X, LayoutGrid, Code2, Database, Play } from 'lucide-react';
import { useStore } from '../../store/useStore';
import SqlEditorTab   from './tabs/SqlEditorTab';
import DataPreviewTab from './tabs/DataPreviewTab';
import DashboardTab   from './tabs/DashboardTab';

const TAB_ICONS = {
  dashboard: LayoutGrid,
  editor:    Code2,
  grid:      Database,
  generator: Play,
};

export default function TabManager() {
  const { tabs, activeTab, closeTab, setActiveTab } = useStore();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: 'var(--color-bg)' }}>

      {/* Tab strip — VS Code style */}
      <div style={{
        display: 'flex', height: 'var(--tab-h)', flexShrink: 0,
        background: 'var(--color-panel)',
        borderBottom: '1px solid var(--color-border)',
        overflowX: 'auto', overflowY: 'hidden',
      }}>
        {tabs.map((tab) => {
          const Icon = TAB_ICONS[tab.type] ?? LayoutGrid;
          const isActive = activeTab === tab.id;
          return (
            <div
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                display: 'flex', alignItems: 'center',
                minWidth: 120, maxWidth: 200,
                height: 'var(--tab-h)',
                padding: '0 12px',
                cursor: 'pointer', userSelect: 'none',
                flexShrink: 0,
                borderRight: '1px solid var(--color-border)',
                borderTop: `2px solid ${isActive ? 'var(--color-primary)' : 'transparent'}`,
                background: isActive ? 'var(--color-bg)' : 'var(--color-panel)',
                color: isActive ? 'var(--color-text)' : 'var(--color-muted)',
                fontSize: 13,
                transition: 'all 150ms',
                position: 'relative',
              }}
              className="group"
            >
              <Icon style={{ width: 14, height: 14, marginRight: 6, flexShrink: 0 }} />
              <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {tab.title}
              </span>
              {/* Close button — only visible on hover or if active */}
              <button
                onClick={(e) => { e.stopPropagation(); closeTab(tab.id); }}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  width: 16, height: 16, marginLeft: 4,
                  border: 'none', background: 'transparent',
                  color: 'var(--color-muted)', cursor: 'pointer', borderRadius: 2,
                  opacity: isActive ? 1 : 0,
                  transition: 'opacity 150ms, background 150ms',
                  flexShrink: 0,
                }}
                className="group-hover:!opacity-100 hover:!bg-border hover:!text-text"
              >
                <X style={{ width: 11, height: 11 }} />
              </button>
            </div>
          );
        })}
      </div>

      {/* Tab content — full height */}
      <div style={{ flex: 1, overflow: 'hidden', position: 'relative', background: 'var(--color-bg)' }}>
        {tabs.length === 0 ? (
          <div style={{
            display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center',
            fontSize: 13, color: 'var(--color-muted)',
          }}>
            No open editors. Click a file in the Explorer to open it.
          </div>
        ) : tabs.map((tab) => (
          <div
            key={tab.id}
            style={{
              position: 'absolute', inset: 0,
              display: activeTab === tab.id ? 'flex' : 'none',
              flexDirection: 'column',
            }}
          >
            {tab.type === 'dashboard' && <DashboardTab />}
            {tab.type === 'editor'    && <SqlEditorTab tab={tab} />}
            {tab.type === 'grid'      && <DataPreviewTab tab={tab} />}
          </div>
        ))}
      </div>
    </div>
  );
}
