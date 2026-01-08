import { useState } from 'react';
import { Plus, Edit, Trash2, Eye, Search, X } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { toast } from 'sonner@2.0.3';

interface CaseStudy {
  id: string;
  title: string;
  client: string;
  description: string;
  challenge: string;
  solution: string;
  results: string;
  technologies: string[];
  category: string;
  image: string;
  date: string;
  published: boolean;
}

export function CaseStudiesManager() {
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingCase, setEditingCase] = useState<CaseStudy | null>(null);

  // Mock data
  const [cases, setCases] = useState<CaseStudy[]>([
    {
      id: '1',
      title: 'E-Commerce Dashboard',
      client: 'TechStart GmbH',
      description: 'Entwicklung eines umfassenden Analytics-Dashboards für E-Commerce',
      challenge: 'Kunde hatte keine Übersicht über Verkaufsdaten und Kundenverhalten',
      solution: 'Implementierung eines Real-Time-Dashboards mit Machine Learning-Prognosen',
      results: '+45% Umsatzsteigerung, -30% Retourenquote durch bessere Insights',
      technologies: ['React', 'Python', 'TensorFlow', 'PostgreSQL'],
      category: 'Datenanalyse',
      image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
      date: '2025-12-15',
      published: true,
    },
    {
      id: '2',
      title: 'Prozessautomatisierung Produktion',
      client: 'Manufacturing AG',
      description: 'Digitalisierung der Produktionsprozesse mit IoT-Integration',
      challenge: 'Manuelle Erfassung führte zu Fehlern und Verzögerungen',
      solution: 'Automatisiertes System mit Sensor-Integration und automatischer Dokumentation',
      results: '+60% Effizienzsteigerung, -80% weniger Fehler',
      technologies: ['Node.js', 'IoT', 'MongoDB', 'Docker'],
      category: 'Digitalisierung',
      image: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800',
      date: '2025-11-20',
      published: true,
    },
    {
      id: '3',
      title: 'CRM-System für Beratung',
      client: 'Consulting Partners',
      description: 'Maßgeschneidertes CRM-System für Unternehmensberatung',
      challenge: 'Verstreute Kundendaten in verschiedenen Systemen',
      solution: 'Zentrales CRM mit Automatisierung und Reporting',
      results: '+35% Produktivität, bessere Kundenbetreuung',
      technologies: ['Django', 'React', 'PostgreSQL', 'Redis'],
      category: 'Softwareentwicklung',
      image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800',
      date: '2025-10-10',
      published: false,
    },
  ]);

  const [formData, setFormData] = useState<Partial<CaseStudy>>({
    title: '',
    client: '',
    description: '',
    challenge: '',
    solution: '',
    results: '',
    technologies: [],
    category: 'Datenanalyse',
    image: '',
    date: new Date().toISOString().split('T')[0],
    published: false,
  });

  const filteredCases = cases.filter(
    (c) =>
      c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.client.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleOpenModal = (caseStudy?: CaseStudy) => {
    if (caseStudy) {
      setEditingCase(caseStudy);
      setFormData(caseStudy);
    } else {
      setEditingCase(null);
      setFormData({
        title: '',
        client: '',
        description: '',
        challenge: '',
        solution: '',
        results: '',
        technologies: [],
        category: 'Datenanalyse',
        image: '',
        date: new Date().toISOString().split('T')[0],
        published: false,
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingCase(null);
  };

  const handleSave = () => {
    if (!formData.title || !formData.client || !formData.description) {
      toast.error('Bitte füllen Sie alle Pflichtfelder aus');
      return;
    }

    if (editingCase) {
      setCases(cases.map((c) => (c.id === editingCase.id ? { ...formData, id: editingCase.id } as CaseStudy : c)));
      toast.success('Case Study aktualisiert');
    } else {
      const newCase: CaseStudy = {
        ...formData,
        id: Date.now().toString(),
      } as CaseStudy;
      setCases([newCase, ...cases]);
      toast.success('Case Study erstellt');
    }
    handleCloseModal();
  };

  const handleDelete = (id: string) => {
    if (confirm('Möchten Sie diese Case Study wirklich löschen?')) {
      setCases(cases.filter((c) => c.id !== id));
      toast.success('Case Study gelöscht');
    }
  };

  const togglePublished = (id: string) => {
    setCases(cases.map((c) => (c.id === id ? { ...c, published: !c.published } : c)));
    toast.success('Status aktualisiert');
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Case Studies</h1>
          <p className="text-zinc-400">Verwalten Sie Ihre Projekt-Referenzen</p>
        </div>
        <Button
          onClick={() => handleOpenModal()}
          className="bg-[#f7931a] hover:bg-[#f7931a]/90 text-white"
        >
          <Plus className="w-5 h-5 mr-2" />
          Neue Case Study
        </Button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
        <input
          type="text"
          placeholder="Suche nach Titel oder Kunde..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#f7931a]/50"
        />
      </div>

      {/* Cases Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCases.map((caseStudy) => (
          <div
            key={caseStudy.id}
            className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl overflow-hidden hover:border-zinc-700 transition-all"
          >
            <div className="relative h-48 bg-zinc-800">
              <img
                src={caseStudy.image}
                alt={caseStudy.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute top-3 right-3">
                <div
                  className={`px-3 py-1 rounded-full text-xs ${
                    caseStudy.published
                      ? 'bg-green-400/20 text-green-400'
                      : 'bg-zinc-700/50 text-zinc-400'
                  }`}
                >
                  {caseStudy.published ? 'Veröffentlicht' : 'Entwurf'}
                </div>
              </div>
            </div>

            <div className="p-5 space-y-3">
              <div>
                <h3 className="font-semibold text-white mb-1">{caseStudy.title}</h3>
                <p className="text-sm text-zinc-400">{caseStudy.client}</p>
              </div>

              <p className="text-sm text-zinc-400 line-clamp-2">{caseStudy.description}</p>

              <div className="flex flex-wrap gap-2">
                {caseStudy.technologies.slice(0, 3).map((tech, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-zinc-800/50 text-zinc-400 text-xs rounded"
                  >
                    {tech}
                  </span>
                ))}
                {caseStudy.technologies.length > 3 && (
                  <span className="px-2 py-1 bg-zinc-800/50 text-zinc-400 text-xs rounded">
                    +{caseStudy.technologies.length - 3}
                  </span>
                )}
              </div>

              <div className="flex gap-2 pt-3 border-t border-zinc-800">
                <button
                  onClick={() => togglePublished(caseStudy.id)}
                  className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-zinc-800/50 rounded-lg hover:bg-zinc-800 transition-colors text-sm text-zinc-300"
                >
                  <Eye className="w-4 h-4" />
                  {caseStudy.published ? 'Verstecken' : 'Veröffentlichen'}
                </button>
                <button
                  onClick={() => handleOpenModal(caseStudy)}
                  className="px-3 py-2 bg-zinc-800/50 rounded-lg hover:bg-zinc-800 transition-colors"
                >
                  <Edit className="w-4 h-4 text-[#f7931a]" />
                </button>
                <button
                  onClick={() => handleDelete(caseStudy.id)}
                  className="px-3 py-2 bg-zinc-800/50 rounded-lg hover:bg-red-400/10 transition-colors"
                >
                  <Trash2 className="w-4 h-4 text-red-400" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredCases.length === 0 && (
        <div className="text-center py-12 text-zinc-500">Keine Case Studies gefunden</div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-zinc-900 border-b border-zinc-800 p-6 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">
                {editingCase ? 'Case Study bearbeiten' : 'Neue Case Study'}
              </h2>
              <button onClick={handleCloseModal} className="text-zinc-400 hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">
                    Titel *
                  </label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="E-Commerce Dashboard"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">
                    Kunde *
                  </label>
                  <input
                    type="text"
                    value={formData.client}
                    onChange={(e) => setFormData({ ...formData, client: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                    placeholder="TechStart GmbH"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">
                  Beschreibung *
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50 resize-none"
                  placeholder="Kurze Beschreibung des Projekts..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">
                  Herausforderung
                </label>
                <textarea
                  value={formData.challenge}
                  onChange={(e) => setFormData({ ...formData, challenge: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50 resize-none"
                  placeholder="Was war die Herausforderung?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">Lösung</label>
                <textarea
                  value={formData.solution}
                  onChange={(e) => setFormData({ ...formData, solution: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50 resize-none"
                  placeholder="Wie haben Sie das Problem gelöst?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">
                  Ergebnisse
                </label>
                <textarea
                  value={formData.results}
                  onChange={(e) => setFormData({ ...formData, results: e.target.value })}
                  rows={2}
                  className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50 resize-none"
                  placeholder="+45% Umsatzsteigerung, -30% Retourenquote"
                />
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">
                    Kategorie
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                  >
                    <option value="Datenanalyse">Datenanalyse</option>
                    <option value="Softwareentwicklung">Softwareentwicklung</option>
                    <option value="Digitalisierung">Digitalisierung</option>
                    <option value="Beratung">Beratung & Strategie</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Datum</label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">
                  Technologien (kommagetrennt)
                </label>
                <input
                  type="text"
                  value={formData.technologies?.join(', ')}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      technologies: e.target.value.split(',').map((t) => t.trim()),
                    })
                  }
                  className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                  placeholder="React, Python, TensorFlow, PostgreSQL"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-2">
                  Bild-URL
                </label>
                <input
                  type="url"
                  value={formData.image}
                  onChange={(e) => setFormData({ ...formData, image: e.target.value })}
                  className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                  placeholder="https://images.unsplash.com/..."
                />
              </div>

              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="published"
                  checked={formData.published}
                  onChange={(e) => setFormData({ ...formData, published: e.target.checked })}
                  className="w-5 h-5 bg-zinc-800 border-zinc-700 rounded focus:ring-[#f7931a]"
                />
                <label htmlFor="published" className="text-zinc-300">
                  Sofort veröffentlichen
                </label>
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
                {editingCase ? 'Aktualisieren' : 'Erstellen'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
