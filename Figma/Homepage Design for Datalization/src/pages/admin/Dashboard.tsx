import { Mail, BookOpen, Users, FileText, TrendingUp, Clock } from 'lucide-react';

interface DashboardProps {
  onNavigate: (section: string) => void;
}

export function Dashboard({ onNavigate }: DashboardProps) {
  const stats = [
    {
      icon: Mail,
      label: 'Kontaktanfragen',
      value: '12',
      change: '+3 diese Woche',
      color: 'text-blue-400',
      bgColor: 'bg-blue-400/10',
    },
    {
      icon: BookOpen,
      label: 'Case Studies',
      value: '8',
      change: '2 in Bearbeitung',
      color: 'text-green-400',
      bgColor: 'bg-green-400/10',
    },
    {
      icon: Users,
      label: 'Kunden',
      value: '24',
      change: '+5 diesen Monat',
      color: 'text-purple-400',
      bgColor: 'bg-purple-400/10',
    },
    {
      icon: FileText,
      label: 'Inhalte',
      value: '45',
      change: 'Zuletzt aktualisiert',
      color: 'text-[#f7931a]',
      bgColor: 'bg-[#f7931a]/10',
    },
  ];

  const recentActivities = [
    {
      type: 'contact',
      message: 'Neue Kontaktanfrage von Max Mustermann',
      time: 'Vor 2 Stunden',
    },
    {
      type: 'case',
      message: 'Case Study "E-Commerce Dashboard" veröffentlicht',
      time: 'Vor 5 Stunden',
    },
    {
      type: 'customer',
      message: 'Neuer Kunde "TechStart GmbH" hinzugefügt',
      time: 'Vor 1 Tag',
    },
    {
      type: 'content',
      message: 'Service-Beschreibung "Datenanalyse" aktualisiert',
      time: 'Vor 2 Tagen',
    },
  ];

  const quickActions = [
    {
      icon: Mail,
      label: 'Kontaktanfragen',
      description: 'Anfragen verwalten',
      onClick: () => onNavigate('contacts'),
    },
    {
      icon: BookOpen,
      label: 'Case Studies',
      description: 'Projekte verwalten',
      onClick: () => onNavigate('cases'),
    },
    {
      icon: Users,
      label: 'Kunden',
      description: 'Kundendaten verwalten',
      onClick: () => onNavigate('customers'),
    },
    {
      icon: FileText,
      label: 'Inhalte',
      description: 'Texte bearbeiten',
      onClick: () => onNavigate('content'),
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-zinc-400">Willkommen zurück! Hier ist eine Übersicht.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={index}
            className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 hover:border-zinc-700 transition-all"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
              <TrendingUp className="w-5 h-5 text-green-400" />
            </div>
            <div className="space-y-1">
              <p className="text-2xl font-bold text-white">{stat.value}</p>
              <p className="text-sm text-zinc-400">{stat.label}</p>
              <p className="text-xs text-zinc-500">{stat.change}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">Schnellzugriff</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={action.onClick}
              className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 hover:border-[#f7931a]/50 hover:bg-zinc-900/70 transition-all group text-left"
            >
              <action.icon className="w-8 h-8 text-[#f7931a] mb-3 group-hover:scale-110 transition-transform" />
              <h3 className="font-semibold text-white mb-1">{action.label}</h3>
              <p className="text-sm text-zinc-400">{action.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Activities */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">Letzte Aktivitäten</h2>
        <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl overflow-hidden">
          {recentActivities.map((activity, index) => (
            <div
              key={index}
              className="p-4 border-b border-zinc-800 last:border-b-0 hover:bg-zinc-800/30 transition-colors"
            >
              <div className="flex items-start gap-3">
                <Clock className="w-5 h-5 text-zinc-500 mt-0.5" />
                <div className="flex-1">
                  <p className="text-white text-sm">{activity.message}</p>
                  <p className="text-xs text-zinc-500 mt-1">{activity.time}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
