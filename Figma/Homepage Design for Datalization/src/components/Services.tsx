import { motion } from 'motion/react';
import { BarChart3, Code, Database, TrendingUp, ArrowRight } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface ServicesProps {
  language: 'de' | 'en';
  onServiceClick?: (serviceId: string) => void;
}

const translations = {
  de: {
    title: 'Unsere Lösungen',
    subtitle: 'Massgeschneiderte Dienstleistungen für Ihre digitale Zukunft',
    learnMore: 'Mehr erfahren',
    services: [
      {
        id: 'data-analytics',
        icon: Database,
        title: 'Datenanalyse',
        description: 'Verwandeln Sie Rohdaten in wertvolle Erkenntnisse. Wir analysieren, interpretieren und visualisieren Ihre Daten für fundierte Entscheidungen.',
        features: ['Business Intelligence', 'Predictive Analytics', 'Data Visualization', 'Reporting'],
        image: 'https://images.unsplash.com/photo-1759661966728-4a02e3c6ed91?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwdmlzdWFsaXphdGlvbiUyMGRhc2hib2FyZHxlbnwxfHx8fDE3Njc4MzU1MDV8MA&ixlib=rb-4.1.0&q=80&w=1080',
      },
      {
        id: 'software',
        icon: Code,
        title: 'Softwareentwicklung',
        description: 'Individuelle Softwarelösungen, die perfekt auf Ihre Bedürfnisse zugeschnitten sind. Von der Konzeption bis zur Implementierung.',
        features: ['Web-Applikationen', 'Automatisierung', 'API-Integration', 'Cloud-Lösungen'],
        image: 'https://images.unsplash.com/photo-1531498860502-7c67cf02f657?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzb2Z0d2FyZSUyMGRldmVsb3BtZW50JTIwY29kZXxlbnwxfHx8fDE3Njc4MTk4NTl8MA&ixlib=rb-4.1.0&q=80&w=1080',
      },
      {
        id: 'digitalization',
        icon: TrendingUp,
        title: 'Digitalisierung',
        description: 'Optimieren Sie Ihre Geschäftsprozesse durch intelligente Digitalisierung. Effizienter, schneller, zukunftsorientiert.',
        features: ['Prozessoptimierung', 'Workflow-Automatisierung', 'Digitale Transformation', 'Change Management'],
        image: 'https://images.unsplash.com/photo-1726607424623-6d9fee974241?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdHJhbnNmb3JtYXRpb24lMjBidXNpbmVzc3xlbnwxfHx8fDE3Njc3OTk0MDl8MA&ixlib=rb-4.1.0&q=80&w=1080',
      },
      {
        id: 'consulting',
        icon: BarChart3,
        title: 'Beratung & Strategie',
        description: 'Strategische Beratung für Ihre datengetriebene Zukunft. Wir entwickeln mit Ihnen den optimalen Weg zur Digitalisierung.',
        features: ['Daten-Strategie', 'IT-Consulting', 'ROI-Optimierung', 'Technologie-Evaluation'],
        image: 'https://images.unsplash.com/photo-1765438869297-6fa4b627906a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMHN0cmF0ZWd5JTIwcGxhbm5pbmd8ZW58MXx8fHwxNzY3ODUxODI4fDA&ixlib=rb-4.1.0&q=80&w=1080',
      },
    ],
  },
  en: {
    title: 'Our Solutions',
    subtitle: 'Tailored services for your digital future',
    learnMore: 'Learn More',
    services: [
      {
        id: 'data-analytics',
        icon: Database,
        title: 'Data Analysis',
        description: 'Transform raw data into valuable insights. We analyze, interpret and visualize your data for informed decisions.',
        features: ['Business Intelligence', 'Predictive Analytics', 'Data Visualization', 'Reporting'],
        image: 'https://images.unsplash.com/photo-1759661966728-4a02e3c6ed91?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwdmlzdWFsaXphdGlvbiUyMGRhc2hib2FyZHxlbnwxfHx8fDE3Njc4MzU1MDV8MA&ixlib=rb-4.1.0&q=80&w=1080',
      },
      {
        id: 'software',
        icon: Code,
        title: 'Software Development',
        description: 'Custom software solutions perfectly tailored to your needs. From concept to implementation.',
        features: ['Web Applications', 'Automation', 'API Integration', 'Cloud Solutions'],
        image: 'https://images.unsplash.com/photo-1531498860502-7c67cf02f657?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzb2Z0d2FyZSUyMGRldmVsb3BtZW50JTIwY29kZXxlbnwxfHx8fDE3Njc4MTk4NTl8MA&ixlib=rb-4.1.0&q=80&w=1080',
      },
      {
        id: 'digitalization',
        icon: TrendingUp,
        title: 'Digitalization',
        description: 'Optimize your business processes through intelligent digitalization. More efficient, faster, future-oriented.',
        features: ['Process Optimization', 'Workflow Automation', 'Digital Transformation', 'Change Management'],
        image: 'https://images.unsplash.com/photo-1726607424623-6d9fee974241?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdHJhbnNmb3JtYXRpb24lMjBidXNpbmVzc3xlbnwxfHx8fDE3Njc3OTk0MDl8MA&ixlib=rb-4.1.0&q=80&w=1080',
      },
      {
        id: 'consulting',
        icon: BarChart3,
        title: 'Consulting & Strategy',
        description: 'Strategic consulting for your data-driven future. We develop the optimal path to digitalization with you.',
        features: ['Data Strategy', 'IT Consulting', 'ROI Optimization', 'Technology Evaluation'],
        image: 'https://images.unsplash.com/photo-1765438869297-6fa4b627906a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMHN0cmF0ZWd5JTIwcGxhbm5pbmd8ZW58MXx8fHwxNzY3ODUxODI4fDA&ixlib=rb-4.1.0&q=80&w=1080',
      },
    ],
  },
};

export function Services({ language, onServiceClick }: ServicesProps) {
  const t = translations[language];

  return (
    <section id="services" className="py-24 scroll-mt-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4">{t.title}</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">{t.subtitle}</p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {t.services.map((service, index) => {
            const Icon = service.icon;
            return (
              <motion.div
                key={service.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-card border border-border rounded-2xl overflow-hidden hover:border-primary/50 transition-all group"
              >
                {/* Service Image */}
                <div className="relative h-48 overflow-hidden">
                  <ImageWithFallback
                    src={service.image}
                    alt={service.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-zinc-950/50 to-transparent"></div>
                </div>

                {/* Content */}
                <div className="p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:bg-primary/20 transition-colors">
                      <Icon className="w-7 h-7 text-primary" />
                    </div>
                    <div>
                      <h3 className="text-2xl mb-2">{service.title}</h3>
                    </div>
                  </div>
                  <p className="text-muted-foreground mb-6">{service.description}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {service.features.map((feature) => (
                      <span
                        key={feature}
                        className="px-3 py-1 bg-secondary border border-border rounded-full text-sm"
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                  {onServiceClick && (
                    <button
                      className="group inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium"
                      onClick={() => onServiceClick(service.id)}
                    >
                      {t.learnMore}
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </button>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}