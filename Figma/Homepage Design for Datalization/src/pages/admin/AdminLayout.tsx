import { useState } from 'react';
import {
  LayoutDashboard,
  Mail,
  BookOpen,
  Users,
  FileText,
  LogOut,
  Menu,
  X,
} from 'lucide-react';
import logo from 'figma:asset/9c79fd0c49d5bb3ae17428ccf646e5ea86915053.png';

interface AdminLayoutProps {
  children: React.ReactNode;
  currentSection: string;
  onNavigate: (section: string) => void;
  onLogout: () => void;
}

export function AdminLayout({ children, currentSection, onNavigate, onLogout }: AdminLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'contacts', label: 'Kontaktanfragen', icon: Mail },
    { id: 'cases', label: 'Case Studies', icon: BookOpen },
    { id: 'customers', label: 'Kunden', icon: Users },
    { id: 'content', label: 'Inhalte', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Top Bar */}
      <div className="fixed top-0 left-0 right-0 h-16 bg-zinc-900 border-b border-zinc-800 z-50">
        <div className="flex items-center justify-between h-full px-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden p-2 hover:bg-zinc-800 rounded-lg transition-colors"
            >
              {sidebarOpen ? (
                <X className="w-6 h-6 text-white" />
              ) : (
                <Menu className="w-6 h-6 text-white" />
              )}
            </button>
            <div className="flex items-center gap-3">
              <img src={logo} alt="Datalization" className="w-8 h-8" />
              <div>
                <h1 className="text-white font-semibold">Datalization</h1>
                <p className="text-xs text-zinc-400">Admin Panel</p>
              </div>
            </div>
          </div>

          <button
            onClick={onLogout}
            className="flex items-center gap-2 px-4 py-2 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-lg transition-all"
          >
            <LogOut className="w-5 h-5" />
            <span className="hidden sm:inline">Abmelden</span>
          </button>
        </div>
      </div>

      {/* Sidebar */}
      <div
        className={`fixed top-16 left-0 bottom-0 w-64 bg-zinc-900 border-r border-zinc-800 transform transition-transform lg:translate-x-0 z-40 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <nav className="p-4 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentSection === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  setSidebarOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-[#f7931a] text-white'
                    : 'text-zinc-400 hover:bg-zinc-800 hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          className="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-30 top-16"
        />
      )}

      {/* Main Content */}
      <div className="pt-16 lg:pl-64">
        <main className="p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}
