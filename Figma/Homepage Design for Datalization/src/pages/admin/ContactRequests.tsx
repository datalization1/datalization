import { useState } from 'react';
import { Mail, Phone, Calendar, CheckCircle, Clock, XCircle, Search, Filter } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { toast } from 'sonner@2.0.3';

interface Contact {
  id: string;
  name: string;
  email: string;
  phone: string;
  service: string;
  message: string;
  status: 'new' | 'in-progress' | 'completed' | 'archived';
  date: string;
}

export function ContactRequests() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [selectedContact, setSelectedContact] = useState<Contact | null>(null);

  // Mock data - in production, this would come from a database
  const [contacts, setContacts] = useState<Contact[]>([
    {
      id: '1',
      name: 'Max Mustermann',
      email: 'max@example.com',
      phone: '+41 79 123 45 67',
      service: 'Datenanalyse & Data Science',
      message: 'Ich bin interessiert an einer Datenanalyse-Lösung für mein Unternehmen. Können wir einen Termin vereinbaren?',
      status: 'new',
      date: '2026-01-08',
    },
    {
      id: '2',
      name: 'Anna Schmidt',
      email: 'anna.schmidt@techcorp.ch',
      phone: '+41 78 987 65 43',
      service: 'Softwareentwicklung',
      message: 'Wir benötigen eine Web-Applikation für unser CRM-System.',
      status: 'in-progress',
      date: '2026-01-07',
    },
    {
      id: '3',
      name: 'Peter Müller',
      email: 'p.mueller@startup.ch',
      phone: '+41 76 555 44 33',
      service: 'Digitalisierung',
      message: 'Interessiert an Prozessautomatisierung für unsere Produktion.',
      status: 'completed',
      date: '2026-01-05',
    },
    {
      id: '4',
      name: 'Sarah Wagner',
      email: 'sarah.w@consulting.ch',
      phone: '+41 77 222 11 00',
      service: 'Beratung & Strategie',
      message: 'Suchen nach strategischer Beratung für unsere Digital-Transformation.',
      status: 'new',
      date: '2026-01-06',
    },
  ]);

  const statusConfig = {
    new: { label: 'Neu', color: 'text-blue-400', bgColor: 'bg-blue-400/10', icon: Clock },
    'in-progress': { label: 'In Bearbeitung', color: 'text-yellow-400', bgColor: 'bg-yellow-400/10', icon: Clock },
    completed: { label: 'Abgeschlossen', color: 'text-green-400', bgColor: 'bg-green-400/10', icon: CheckCircle },
    archived: { label: 'Archiviert', color: 'text-zinc-500', bgColor: 'bg-zinc-500/10', icon: XCircle },
  };

  const filteredContacts = contacts.filter((contact) => {
    const matchesSearch =
      contact.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      contact.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || contact.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const updateStatus = (contactId: string, newStatus: Contact['status']) => {
    setContacts(contacts.map((c) => (c.id === contactId ? { ...c, status: newStatus } : c)));
    toast.success('Status aktualisiert');
  };

  const deleteContact = (contactId: string) => {
    if (confirm('Möchten Sie diese Anfrage wirklich löschen?')) {
      setContacts(contacts.filter((c) => c.id !== contactId));
      setSelectedContact(null);
      toast.success('Anfrage gelöscht');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Kontaktanfragen</h1>
        <p className="text-zinc-400">Verwalten Sie alle eingehenden Anfragen</p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
          <input
            type="text"
            placeholder="Suche nach Name oder Email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#f7931a]/50"
          />
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="pl-10 pr-8 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50 appearance-none cursor-pointer"
          >
            <option value="all">Alle Status</option>
            <option value="new">Neu</option>
            <option value="in-progress">In Bearbeitung</option>
            <option value="completed">Abgeschlossen</option>
            <option value="archived">Archiviert</option>
          </select>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {Object.entries(statusConfig).map(([status, config]) => {
          const count = contacts.filter((c) => c.status === status).length;
          return (
            <div
              key={status}
              className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-lg p-4"
            >
              <div className={`flex items-center gap-2 mb-2 ${config.color}`}>
                <config.icon className="w-5 h-5" />
                <span className="text-2xl font-bold">{count}</span>
              </div>
              <p className="text-sm text-zinc-400">{config.label}</p>
            </div>
          );
        })}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Contacts List */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-white">
            Anfragen ({filteredContacts.length})
          </h2>
          <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
            {filteredContacts.map((contact) => {
              const config = statusConfig[contact.status];
              return (
                <div
                  key={contact.id}
                  onClick={() => setSelectedContact(contact)}
                  className={`bg-zinc-900/50 backdrop-blur-sm border rounded-xl p-4 cursor-pointer transition-all ${
                    selectedContact?.id === contact.id
                      ? 'border-[#f7931a]'
                      : 'border-zinc-800 hover:border-zinc-700'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="font-semibold text-white">{contact.name}</h3>
                      <p className="text-sm text-zinc-400">{contact.email}</p>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-xs ${config.bgColor} ${config.color}`}>
                      {config.label}
                    </div>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-zinc-500">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {new Date(contact.date).toLocaleDateString('de-CH')}
                    </div>
                  </div>
                  <p className="text-sm text-zinc-400 mt-2 line-clamp-2">{contact.message}</p>
                </div>
              );
            })}
            {filteredContacts.length === 0 && (
              <div className="text-center py-12 text-zinc-500">
                Keine Anfragen gefunden
              </div>
            )}
          </div>
        </div>

        {/* Contact Details */}
        <div>
          <h2 className="text-lg font-semibold text-white mb-4">Details</h2>
          {selectedContact ? (
            <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 space-y-6">
              <div>
                <h3 className="text-xl font-semibold text-white mb-1">
                  {selectedContact.name}
                </h3>
                <div className={`inline-flex px-3 py-1 rounded-full text-xs ${statusConfig[selectedContact.status].bgColor} ${statusConfig[selectedContact.status].color}`}>
                  {statusConfig[selectedContact.status].label}
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center gap-3 text-zinc-300">
                  <Mail className="w-5 h-5 text-zinc-500" />
                  <a href={`mailto:${selectedContact.email}`} className="hover:text-[#f7931a]">
                    {selectedContact.email}
                  </a>
                </div>
                <div className="flex items-center gap-3 text-zinc-300">
                  <Phone className="w-5 h-5 text-zinc-500" />
                  <a href={`tel:${selectedContact.phone}`} className="hover:text-[#f7931a]">
                    {selectedContact.phone}
                  </a>
                </div>
                <div className="flex items-center gap-3 text-zinc-300">
                  <Calendar className="w-5 h-5 text-zinc-500" />
                  {new Date(selectedContact.date).toLocaleDateString('de-CH', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric',
                  })}
                </div>
              </div>

              <div>
                <h4 className="text-sm font-semibold text-zinc-400 mb-2">Service</h4>
                <p className="text-white">{selectedContact.service}</p>
              </div>

              <div>
                <h4 className="text-sm font-semibold text-zinc-400 mb-2">Nachricht</h4>
                <p className="text-zinc-300 leading-relaxed">{selectedContact.message}</p>
              </div>

              <div className="pt-4 border-t border-zinc-800 space-y-3">
                <h4 className="text-sm font-semibold text-zinc-400">Status ändern</h4>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(statusConfig).map(([status, config]) => (
                    <button
                      key={status}
                      onClick={() => updateStatus(selectedContact.id, status as Contact['status'])}
                      className={`px-4 py-2 rounded-lg border transition-all ${
                        selectedContact.status === status
                          ? `${config.bgColor} ${config.color} border-current`
                          : 'border-zinc-700 text-zinc-400 hover:border-zinc-600'
                      }`}
                    >
                      {config.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-zinc-800">
                <Button
                  onClick={() => deleteContact(selectedContact.id)}
                  variant="ghost"
                  className="w-full text-red-400 hover:bg-red-400/10 hover:text-red-400"
                >
                  Anfrage löschen
                </Button>
              </div>
            </div>
          ) : (
            <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-12 text-center text-zinc-500">
              Wählen Sie eine Anfrage aus, um Details anzuzeigen
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
