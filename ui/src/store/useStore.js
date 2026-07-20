import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useStore = create(
  persist(
    (set) => ({
      // ── Tab Management ────────────────────────────────────────────────────
      tabs: [{ id: 'dashboard', title: 'Dashboard', type: 'dashboard' }],
      activeTab: 'dashboard',

      openTab: (tab) => set((state) => {
        const exists = state.tabs.find(t => t.id === tab.id);
        if (!exists) return { tabs: [...state.tabs, tab], activeTab: tab.id };
        return { activeTab: tab.id };
      }),

      closeTab: (id) => set((state) => {
        const newTabs  = state.tabs.filter(t => t.id !== id);
        let newActive  = state.activeTab;
        if (state.activeTab === id) {
          newActive = newTabs.length > 0 ? newTabs[newTabs.length - 1].id : null;
        }
        return { tabs: newTabs, activeTab: newActive };
      }),

      setActiveTab: (id) => set({ activeTab: id }),

      // ── Logs ─────────────────────────────────────────────────────────────
      logs: [],
      addLog: (log) => set((state) => ({
        logs: [...state.logs, { ...log, timestamp: new Date().toLocaleTimeString() }]
      })),
      clearLogs: () => set({ logs: [] }),

      // ── Auth / User (role-aware) ──────────────────────────────────────────
      // user shape: { name, email, role }
      user: null,
      login:  (user) => set({ user }),
      logout: () => set({ user: null, tabs: [{ id: 'dashboard', title: 'Dashboard', type: 'dashboard' }], activeTab: 'dashboard' }),
    }),
    {
      name: 'ets-store',
      partialize: (state) => ({ user: state.user }), // only persist user session
    }
  )
)
