import { useState } from 'react';
import { Plus, Edit, Trash2, Building, Mail, Phone, Calendar, Search, X } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { toast } from 'sonner@2.0.3';

interface Customer {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  industry: string;
  status: 'active' | 'inactive' | 'prospect';
  projectsCount: number;
  revenue: string;
  startDate: string;
  notes: string;
}

export function CustomersManager() {
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null);

  const [customers, setCustomers] = useState<Customer[]>([
    {
      id: '1',
      name: 'Max Mustermann',
      company: 'TechStart GmbH',
      email: 'max@techstart.ch',
      phone: '+41 79 123 45 67',
      industry: 'E-Commerce',
      status: 'active',
      projectsCount: 3,
      revenue: 'CHF 45\'000',
      startDate: '2024-06-15',
      notes: 'Sehr zufriedener Kunde, plant weitere Projekte',
    },
    {
      id: '2',
      name: 'Anna Schmidt',
      company: 'Manufacturing AG',
      email: 'anna@manufacturing.ch',
      phone: '+41 78 987 65 43',
      industry: 'Produktion',
      status: 'active',
      projectsCount: 1,
      revenue: 'CHF 28\'000',
      startDate: '2025-03-20',
      notes: 'Automatisierung der Produktionsprozesse',
    },
    {
      id: '3',
      name: 'Peter Wagner',
      company: 'Consulting Partners',
      email: 'peter@consulting.ch',
      phone: '+41 76 555 44 33',
      industry: 'Beratung',
      status: 'active',
      projectsCount: 2,
      revenue: 'CHF 32\'000',
      startDate: '2024-11-10',
      notes: 'CRM-System und Prozessoptimierung',
    },
    {
      id: '4',
      name: 'Sarah Meier',
      company: 'FinTech Solutions',
      email: 'sarah@fintech.ch',
      phone: '+41 77 222 11 00',
      industry: 'Finanzdienstleistungen',
      status: 'prospect',
      projectsCount: 0,
      revenue: 'CHF 0',
      startDate: '2026-01-05',
      notes: 'Interessiert an Datenanalyse-Lösungen',
    },
  ]);

  const [formData, setFormData] = useState<Partial<Customer>>({
    name: '',
    company: '',
    email: '',
    phone: '',
    industry: '',
    status: 'prospect',
    projectsCount: 0,
    revenue: '',
    startDate: new Date().toISOString().split('T')[0],
    notes: '',
  });

  const statusConfig = {
    active: { label: 'Aktiv', color: 'text-green-400', bgColor: 'bg-green-400/10' },
    inactive: { label: 'Inaktiv', color: 'text-zinc-500', bgColor: 'bg-zinc-500/10' },
    prospect: { label: 'Interessent', color: 'text-blue-400', bgColor: 'bg-blue-400/10' },
  };

  const filteredCustomers = customers.filter(
    (c) =>
      c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleOpenModal = (customer?: Customer) => {
    if (customer) {
      setEditingCustomer(customer);
      setFormData(customer);
    } else {
      setEditingCustomer(null);
      setFormData({
        name: '',
        company: '',
        email: '',
        phone: '',
        industry: '',
        status: 'prospect',
        projectsCount: 0,
        revenue: '',
        startDate: new Date().toISOString().split('T')[0],
        notes: '',
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingCustomer(null);
  };

  const handleSave = () => {
    if (!formData.name || !formData.company || !formData.email) {
      toast.error('Bitte füllen Sie alle Pflichtfelder aus');
      return;
    }

    if (editingCustomer) {
      setCustomers(
        customers.map((c) =>
          c.id === editingCustomer.id ? ({ ...formData, id: editingCustomer.id } as Customer) : c
        )
      );
      toast.success('Kunde aktualisiert');
    } else {
      const newCustomer: Customer = {
        ...formData,
        id: Date.now().toString(),
      } as Customer;
      setCustomers([newCustomer, ...customers]);
      toast.success('Kunde hinzugefügt');
    }
    handleCloseModal();
  };

  const handleDelete = (id: string) => {
    if (confirm('Möchten Sie diesen Kunden wirklich löschen?')) {
      setCustomers(customers.filter((c) => c.id !== id));
      toast.success('Kunde gelöscht');
    }
  };

  const totalRevenue = customers.reduce((sum, c) => {
    const amount = parseInt(c.revenue.replace(/[^\d]/g, '')) || 0;
    return sum + amount;
  }, 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Kunden</h1>
          <p className="text-zinc-400">Verwalten Sie Ihre Kundendaten</p>
        </div>
        <Button
          onClick={() => handleOpenModal()}
          className="bg-[#f7931a] hover:bg-[#f7931a]/90 text-white"
        >
          <Plus className="w-5 h-5 mr-2" />
          Neuer Kunde
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-green-400/10 rounded-lg">
              <Building className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{customers.length}</p>
              <p className="text-sm text-zinc-400">Gesamt Kunden</p>
            </div>
          </div>
        </div>

        <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-400/10 rounded-lg">
              <Building className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">
                {customers.filter((c) => c.status === 'active').length}
              </p>
              <p className="text-sm text-zinc-400">Aktive Kunden</p>
            </div>
          </div>
        </div>

        <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-[#f7931a]/10 rounded-lg">
              <Building className="w-5 h-5 text-[#f7931a]" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">
                CHF {totalRevenue.toLocaleString('de-CH')}
              </p>
              <p className="text-sm text-zinc-400">Gesamtumsatz</p>
            </div>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
        <input
          type="text"
          placeholder="Suche nach Name, Firma oder Email..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#f7931a]/50"
        />
      </div>

      {/* Customers Table */}
      <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-zinc-800">
                <th className="text-left p-4 text-sm font-semibold text-zinc-400">Kunde</th>
                <th className="text-left p-4 text-sm font-semibold text-zinc-400">Kontakt</th>
                <th className="text-left p-4 text-sm font-semibold text-zinc-400">Branche</th>
                <th className="text-left p-4 text-sm font-semibold text-zinc-400">Status</th>
                <th className="text-left p-4 text-sm font-semibold text-zinc-400">Projekte</th>
                <th className="text-left p-4 text-sm font-semibold text-zinc-400">Umsatz</th>
                <th className="text-right p-4 text-sm font-semibold text-zinc-400">Aktionen</th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.map((customer) => {
                const config = statusConfig[customer.status];
                return (
                  <tr
                    key={customer.id}
                    className="border-b border-zinc-800 last:border-b-0 hover:bg-zinc-800/30 transition-colors"
                  >
                    <td className="p-4">
                      <div>
                        <p className="font-semibold text-white">{customer.name}</p>
                        <p className="text-sm text-zinc-400">{customer.company}</p>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 text-sm text-zinc-400">
                          <Mail className="w-4 h-4" />
                          {customer.email}
                        </div>
                        <div className="flex items-center gap-2 text-sm text-zinc-400">
                          <Phone className="w-4 h-4" />
                          {customer.phone}
                        </div>
                      </div>
                    </td>
                    <td className="p-4">
                      <p className="text-sm text-zinc-300">{customer.industry}</p>
                    </td>
                    <td className="p-4">
                      <div className={`inline-flex px-3 py-1 rounded-full text-xs ${config.bgColor} ${config.color}`}>
                        {config.label}
                      </div>
                    </td>
                    <td className="p-4">
                      <p className="text-white">{customer.projectsCount}</p>
                    </td>
                    <td className="p-4">
                      <p className="text-white font-semibold">{customer.revenue}</p>
                    </td>
                    <td className="p-4">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(customer)}
                          className="p-2 hover:bg-zinc-800 rounded-lg transition-colors"
                        >
                          <Edit className="w-4 h-4 text-[#f7931a]" />
                        </button>
                        <button
                          onClick={() => handleDelete(customer.id)}
                          className="p-2 hover:bg-red-400/10 rounded-lg transition-colors"
                        >
                          <Trash2 className="w-4 h-4 text-red-400" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {filteredCustomers.length === 0 && (
          <div className="text-center py-12 text-zinc-500">Keine Kunden gefunden</div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-zinc-900 border-b border-zinc-800 p-6 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">
                {editingCustomer ? 'Kunde bearbeiten' : 'Neuer Kunde'}
              </h2>
              <button onClick={handleCloseModal} className="text-zinc-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="Max Mustermann"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Firma *</label>
                  <input
                    type="text"
                    value={formData.company}
                    onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="TechStart GmbH"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Email *</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="max@example.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Telefon</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="+41 79 123 45 67"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Branche</label>
                  <input
                    type="text"
                    value={formData.industry}
                    onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="E-Commerce"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Status</label>
                  <select
                    value={formData.status}
                    onChange={(e) =>
                      setFormData({ ...formData, status: e.target.value as Customer['status'] })
                    }
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                  >
                    <option value="prospect">Interessent</option>
                    <option value="active">Aktiv</option>
                    <option value="inactive">Inaktiv</option>
                  </select>
                </div>
              </div>

              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">
                    Anzahl Projekte
                  </label>
                  <input
                    type="number"
                    value={formData.projectsCount}
                    onChange={(e) =>
                      setFormData({ ...formData, projectsCount: parseInt(e.target.value) || 0 })
                    }
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    min="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Umsatz</label>
                  <input
                    type="text"
                    value={formData.revenue}
                    onChange={(e) => setFormData({ ...formData, revenue: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="CHF 45'000"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">
                    Startdatum
                  </label>
                  <input
                    type="date"
                    value={formData.startDate}
                    onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">Notizen</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  rows={4}
                  className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50 resize-none"
                  placeholder="Zusätzliche Informationen..."
                />
              </div>
            </div>

            <div className="sticky bottom-0 bg-zinc-900 border-t border-zinc-800 p-6 flex justify-end gap-3">
              <Button onClick={handleCloseModal} variant="ghost">
                Abbrechen
              </Button>
              <Button
                onClick={handleSave}
                className="bg-[#f7931a] hover:bg-[#f7931a]/90 text-white"
              >
                {editingCustomer ? 'Aktualisieren' : 'Hinzufügen'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
