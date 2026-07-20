import React from 'react';
import * as Resizable from 'react-resizable-panels';
const Panel = Resizable.Panel || Resizable.default?.Panel;
const PanelGroup = Resizable.Group || Resizable.PanelGroup || Resizable.default?.PanelGroup;
const PanelResizeHandle = Resizable.Separator || Resizable.PanelResizeHandle || Resizable.default?.PanelResizeHandle;
import TopHeader from '../components/layout/TopHeader';
import LeftSidebar from '../components/layout/LeftSidebar';
import AiIntelligence from '../components/layout/AiIntelligence';
import BottomOutput from '../components/layout/BottomOutput';
import TabManager from '../components/workspace/TabManager';

export default function IDE() {
  return (
    <div className="flex flex-col h-screen w-full bg-bg overflow-hidden font-sans">
      <TopHeader />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Main Workspace (Top 75%) */}
        <div className="flex-1 flex overflow-hidden">
          {/* Left Explorer (20%) */}
          <div className="w-[300px] flex-shrink-0 border-r border-border bg-panel">
            <LeftSidebar />
          </div>
          
          {/* Center Workspace (Tabs) (60%) */}
          <div className="flex-1 flex flex-col min-w-0 bg-bg">
            <TabManager />
          </div>
          
          {/* AI Intelligence (20%) */}
          <div className="w-[300px] flex-shrink-0 border-l border-border bg-panel hidden xl:block">
            <AiIntelligence />
          </div>
        </div>
        
        {/* Bottom Output (Bottom 25%) */}
        <div className="h-[250px] flex-shrink-0 border-t border-border bg-panel">
          <BottomOutput />
        </div>
      </div>
    </div>
  );
}
