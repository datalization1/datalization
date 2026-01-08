import { useState } from 'react';
import { Save, RotateCcw, Globe } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { toast } from 'sonner@2.0.3';

interface ContentSection {
  id: string;
  section: string;
  key: string;
  de: string;
  en: string;
  type: 'text' | 'textarea';
}

export function ContentManager() {
  const [language, setLanguage] = useState<'de' | 'en'>('de');
  const [hasChanges, setHasChanges] = useState(false);

  const [content, setContent] = useState<ContentSection[]>([
    // Hero Section
    {
      id: '1',
      section: 'Hero',
      key: 'hero.title',
      de: 'Daten in Werte verwandeln',
      en: 'Transform Data into Value',
      type: 'text',
    },
    {
      id: '2',
      section: 'Hero',
      key: 'hero.subtitle',
      de: 'Loyal leben und einfache Lösungen schaffen',
      en: 'Live loyally and create simple solutions',
      type: 'text',
    },
    {
      id: '3',
      section: 'Hero',
      key: 'hero.description',
      de: 'Wir helfen Unternehmen, ihre Daten zu verstehen und zu nutzen, um bessere Entscheidungen zu treffen und nachhaltiges Wachstum zu erreichen.',
      en: 'We help companies understand and use their data to make better decisions and achieve sustainable growth.',
      type: 'textarea',
    },
    // Vision Section
    {
      id: '4',
      section: 'Vision',
      key: 'vision.title',
      de: 'Unsere Vision',
      en: 'Our Vision',
      type: 'text',
    },
    {
      id: '5',
      section: 'Vision',
      key: 'vision.description',
      de: 'Loyal leben und einfache Lösungen schaffen. Wir glauben an die Kraft der Daten und die Bedeutung von klaren, verständlichen Lösungen.',
      en: 'Live loyally and create simple solutions. We believe in the power of data and the importance of clear, understandable solutions.',
      type: 'textarea',
    },
    // Services Section
    {
      id: '6',
      section: 'Services',
      key: 'services.title',
      de: 'Unsere Lösungen',
      en: 'Our Solutions',
      type: 'text',
    },
    {
      id: '7',
      section: 'Services',
      key: 'services.description',
      de: 'Von Datenanalyse bis zur vollständigen Digitalisierung – wir bieten maßgeschneiderte Lösungen für Ihre Herausforderungen.',
      en: 'From data analysis to complete digitalization – we offer tailored solutions for your challenges.',
      type: 'textarea',
    },
    {
      id: '8',
      section: 'Services',
      key: 'services.data_analytics.title',
      de: 'Datenanalyse & Data Science',
      en: 'Data Analytics & Data Science',
      type: 'text',
    },
    {
      id: '9',
      section: 'Services',
      key: 'services.data_analytics.description',
      de: 'Verwandeln Sie Ihre Daten in wertvolle Erkenntnisse mit fortschrittlichen Analysen und Machine Learning.',
      en: 'Transform your data into valuable insights with advanced analytics and machine learning.',
      type: 'textarea',
    },
    {
      id: '10',
      section: 'Services',
      key: 'services.software.title',
      de: 'Softwareentwicklung',
      en: 'Software Development',
      type: 'text',
    },
    {
      id: '11',
      section: 'Services',
      key: 'services.software.description',
      de: 'Maßgeschneiderte Softwarelösungen, die genau auf Ihre Geschäftsprozesse zugeschnitten sind.',
      en: 'Custom software solutions tailored precisely to your business processes.',
      type: 'textarea',
    },
    {
      id: '12',
      section: 'Services',
      key: 'services.digitalization.title',
      de: 'Digitalisierung',
      en: 'Digitalization',
      type: 'text',
    },
    {
      id: '13',
      section: 'Services',
      key: 'services.digitalization.description',
      de: 'Automatisieren Sie Ihre Prozesse und steigern Sie die Effizienz durch intelligente Digitalisierung.',
      en: 'Automate your processes and increase efficiency through intelligent digitalization.',
      type: 'textarea',
    },
    {
      id: '14',
      section: 'Services',
      key: 'services.consulting.title',
      de: 'Beratung & Strategie',
      en: 'Consulting & Strategy',
      type: 'text',
    },
    {
      id: '15',
      section: 'Services',
      key: 'services.consulting.description',
      de: 'Strategische Beratung für Ihre digitale Transformation und nachhaltige Unternehmensentwicklung.',
      en: 'Strategic consulting for your digital transformation and sustainable business development.',
      type: 'textarea',
    },
    // About Section
    {
      id: '16',
      section: 'About',
      key: 'about.title',
      de: 'Wer wir sind',
      en: 'Who We Are',
      type: 'text',
    },
    {
      id: '17',
      section: 'About',
      key: 'about.description',
      de: 'Datalization ist Ihr Partner für Datenanalyse und Digitalisierung. Mit unserer Expertise und Leidenschaft helfen wir Unternehmen, das volle Potenzial ihrer Daten zu nutzen.',
      en: 'Datalization is your partner for data analysis and digitalization. With our expertise and passion, we help companies unlock the full potential of their data.',
      type: 'textarea',
    },
    // Contact Section
    {
      id: '18',
      section: 'Contact',
      key: 'contact.title',
      de: 'Kontakt',
      en: 'Contact',
      type: 'text',
    },
    {
      id: '19',
      section: 'Contact',
      key: 'contact.description',
      de: 'Lassen Sie uns gemeinsam Ihre Herausforderungen besprechen und die passende Lösung finden.',
      en: 'Let\'s discuss your challenges together and find the right solution.',
      type: 'textarea',
    },
    // Footer
    {
      id: '20',
      section: 'Footer',
      key: 'footer.tagline',
      de: 'Loyal leben und einfache Lösungen schaffen',
      en: 'Live loyally and create simple solutions',
      type: 'text',
    },
  ]);

  const [originalContent] = useState<ContentSection[]>(JSON.parse(JSON.stringify(content)));

  const updateContent = (id: string, field: 'de' | 'en', value: string) => {
    setContent(content.map((item) => (item.id === id ? { ...item, [field]: value } : item)));
    setHasChanges(true);
  };

  const handleSave = () => {
    // In production, this would save to a database
    toast.success('Änderungen gespeichert');
    setHasChanges(false);
  };

  const handleReset = () => {
    if (confirm('Möchten Sie alle Änderungen verwerfen?')) {
      setContent(JSON.parse(JSON.stringify(originalContent)));
      setHasChanges(false);
      toast.success('Änderungen zurückgesetzt');
    }
  };

  const sections = [...new Set(content.map((item) => item.section))];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Content Management</h1>
          <p className="text-zinc-400">Bearbeiten Sie alle Texte auf der Website</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-zinc-900/50 border border-zinc-800 rounded-lg p-1">
            <button
              onClick={() => setLanguage('de')}
              className={`px-4 py-2 rounded-lg transition-all ${
                language === 'de'
                  ? 'bg-[#f7931a] text-white'
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              DE
            </button>
            <button
              onClick={() => setLanguage('en')}
              className={`px-4 py-2 rounded-lg transition-all ${
                language === 'en'
                  ? 'bg-[#f7931a] text-white'
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              EN
            </button>
          </div>
        </div>
      </div>

      {hasChanges && (
        <div className="bg-[#f7931a]/10 border border-[#f7931a]/30 rounded-xl p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Globe className="w-5 h-5 text-[#f7931a]" />
            <p className="text-white">Sie haben ungespeicherte Änderungen</p>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={handleReset}
              variant="ghost"
              size="sm"
              className="text-zinc-400 hover:text-white"
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              Zurücksetzen
            </Button>
            <Button
              onClick={handleSave}
              size="sm"
              className="bg-[#f7931a] hover:bg-[#f7931a]/90 text-white"
            >
              <Save className="w-4 h-4 mr-2" />
              Speichern
            </Button>
          </div>
        </div>
      )}

      <div className="space-y-8">
        {sections.map((section) => {
          const sectionItems = content.filter((item) => item.section === section);
          return (
            <div
              key={section}
              className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6"
            >
              <h2 className="text-xl font-semibold text-white mb-6 pb-4 border-b border-zinc-800">
                {section}
              </h2>

              <div className="space-y-6">
                {sectionItems.map((item) => (
                  <div key={item.id} className="space-y-3">
                    <div className="flex items-center justify-between">
                      <label className="block text-sm font-medium text-zinc-400">
                        {item.key}
                      </label>
                      <span className="text-xs text-zinc-500 uppercase">{language}</span>
                    </div>

                    {item.type === 'text' ? (
                      <input
                        type="text"
                        value={language === 'de' ? item.de : item.en}
                        onChange={(e) => updateContent(item.id, language, e.target.value)}
                        className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50"
                      />
                    ) : (
                      <textarea
                        value={language === 'de' ? item.de : item.en}
                        onChange={(e) => updateContent(item.id, language, e.target.value)}
                        rows={3}
                        className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-[#f7931a]/50 resize-none"
                      />
                    )}

                    {/* Show both languages for comparison */}
                    <div className="grid md:grid-cols-2 gap-4 pt-2 pb-4 border-b border-zinc-800 last:border-b-0 last:pb-0">
                      <div className="space-y-1">
                        <p className="text-xs text-zinc-500 uppercase">Deutsch</p>
                        <p className="text-sm text-zinc-400 line-clamp-2">{item.de}</p>
                      </div>
                      <div className="space-y-1">
                        <p className="text-xs text-zinc-500 uppercase">English</p>
                        <p className="text-sm text-zinc-400 line-clamp-2">{item.en}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Sticky Save Bar */}
      {hasChanges && (
        <div className="fixed bottom-0 left-0 right-0 bg-zinc-900 border-t border-zinc-800 p-4 z-40">
          <div className="container mx-auto max-w-7xl flex items-center justify-between">
            <p className="text-white">Ungespeicherte Änderungen</p>
            <div className="flex gap-3">
              <Button onClick={handleReset} variant="ghost">
                Verwerfen
              </Button>
              <Button
                onClick={handleSave}
                className="bg-[#f7931a] hover:bg-[#f7931a]/90 text-white"
              >
                <Save className="w-4 h-4 mr-2" />
                Änderungen speichern
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
