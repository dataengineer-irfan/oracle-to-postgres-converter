import React, { useState, useRef, useEffect } from 'react';
import { Terminal, XCircle, AlertTriangle, CheckCircle, Database, Filter, Search, Eraser, Download, Pause, ArrowDown, Share2 } from 'lucide-react';
import ActionToolbar from '../common/ActionToolbar';
import { useStore } from '../../store/useStore';

export default function BottomOutput() {
  const [activeTab, setActiveTab] = useState('validation');
  const [autoScroll, setAutoScroll] = useState(true);
  
  const logs = useStore(state => state.logs);
  const logsEndRef = useRef(null);

  useEffect(() => {
    if (autoScroll && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, autoScroll, activeTab]);

  const tabs = [
    { id: 'console', label: 'Console', icon: Terminal },
    { id: 'logs', label: 'Logs', icon: Database },
    { id: 'execution', label: 'Execution', icon: CheckCircle },
    { id: 'warnings', label: 'Warnings', icon: AlertTriangle },
    { id: 'errors', label: 'Errors', icon: XCircle },
    { id: 'validation', label: 'Validation', icon: CheckCircle },
  ];

  const getLogIcon = (level) => {
    switch (level) {
      case 'ERROR': return <XCircle className="w-3.5 h-3.5 text-error" />;
      case 'WARNING': return <AlertTriangle className="w-3.5 h-3.5 text-warning" />;
      case 'SUCCESS': return <CheckCircle className="w-3.5 h-3.5 text-success" />;
      default: return <Database className="w-3.5 h-3.5 text-info" />;
    }
  };

  const getLogLevelClass = (level) => {
    switch (level) {
      case 'ERROR': return 'text-error bg-error/10 border-error/20';
      case 'WARNING': return 'text-warning bg-warning/10 border-warning/20';
      case 'SUCCESS': return 'text-success bg-success/10 border-success/20';
      default: return 'text-info bg-info/10 border-info/20';
    }
  };

  return (
    <div className="h-full bg-panel flex flex-col overflow-hidden text-sm select-none border-t border-border shadow-[0_-5px_15px_rgba(0,0,0,0.2)]">
      
      {/* Tabs */}
      <div className="flex bg-panel border-b border-border overflow-x-auto custom-scrollbar flex-shrink-0">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-4 py-2 border-b-2 text-xs font-medium whitespace-nowrap transition-colors ${
                activeTab === tab.id 
                  ? 'border-primary text-primary bg-bg/50' 
                  : 'border-transparent text-muted hover:text-text hover:bg-border/50'
              }`}
            >
              <Icon className="w-3.5 h-3.5 mr-2" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Action Toolbar */}
      <div className="flex-shrink-0">
        <ActionToolbar 
          title={`${tabs.find(t => t.id === activeTab)?.label} Output`} 
          type="LOG" 
        />
      </div>
      
      <div className="flex bg-panel border-b border-border px-2 py-1 items-center justify-between text-muted">
         <div className="flex space-x-1">
            <button className="p-1 hover:bg-border/50 rounded" title="Filter"><Filter className="w-3.5 h-3.5" /></button>
            <button className="p-1 hover:bg-border/50 rounded" title="Search Logs"><Search className="w-3.5 h-3.5" /></button>
         </div>
         <div className="flex space-x-1">
            <button className="p-1 hover:bg-border/50 rounded" title="Clear"><Eraser className="w-3.5 h-3.5" /></button>
            <div className="w-[1px] h-4 bg-border/50 mx-1 mt-0.5"></div>
            <button 
              className={`p-1 rounded flex items-center ${autoScroll ? 'bg-primary/20 text-primary' : 'hover:bg-border/50'}`} 
              onClick={() => setAutoScroll(!autoScroll)}
              title="Auto Scroll"
            >
              <ArrowDown className="w-3.5 h-3.5 mr-1" /><span className="text-[10px]">Auto-Scroll</span>
            </button>
            <button className="p-1 hover:bg-border/50 rounded" title="Pause"><Pause className="w-3.5 h-3.5" /></button>
         </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto custom-scrollbar bg-bg p-0">
        
        {logs.length === 0 ? (
          <div className="flex h-full items-center justify-center text-muted font-mono text-xs opacity-50">
            No logs available.
          </div>
        ) : (
          <div className="font-mono text-[11px] leading-relaxed w-full min-w-max">
            {/* Table Header */}
            <div className="flex items-center text-muted/70 bg-panel px-4 py-1.5 border-b border-border sticky top-0 uppercase tracking-wider font-semibold">
               <div className="w-24 flex-shrink-0">Time</div>
               <div className="w-24 flex-shrink-0">Level</div>
               <div className="flex-1 min-w-[300px]">Message</div>
               <div className="w-24 flex-shrink-0 text-right">Duration</div>
            </div>

            {/* Log Rows */}
            {logs.map((log, index) => (
              <div key={index} className="flex items-center hover:bg-border/30 px-4 py-1.5 border-b border-border/20 transition-colors group">
                <div className="w-24 flex-shrink-0 text-muted">{log.timestamp || new Date().toLocaleTimeString()}</div>
                <div className="w-24 flex-shrink-0">
                  <span className={`px-1.5 py-0.5 rounded border text-[9px] font-bold tracking-wider ${getLogLevelClass(log.level)}`}>
                    {log.level || 'INFO'}
                  </span>
                </div>
                <div className="flex-1 min-w-[300px] text-text flex items-center">
                  <span className="text-muted mr-2">[{log.module || 'System'}]</span> 
                  {log.message}
                </div>
                <div className="w-24 flex-shrink-0 text-right text-muted group-hover:text-text transition-colors">
                  {log.duration || (Math.random() * 3).toFixed(2) + 's'}
                </div>
              </div>
            ))}
            <div ref={logsEndRef} />
          </div>
        )}
      </div>
    </div>
  );
}
