import { motion } from 'motion/react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { ArrowUpRight, CheckCircle } from 'lucide-react';

interface CaseStudiesProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Case Studies',
    subtitle: 'Erfolgsgeschichten unserer Kunden',
    viewMore: 'Mehr erfahren',
    cases: [
      {
        title: 'Analytics Dashboard für KMU',
        category: 'Datenanalyse',
        description: 'Entwicklung eines intuitiven Dashboards zur Echtzeitüberwachung von Geschäftskennzahlen.',
        results: [
          '60% schnellere Entscheidungsfindung',
          'Automatisierte Reporting-Prozesse',
          'Erhöhte Datentransparenz',
        ],
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwYW5hbHl0aWNzJTIwZGFzaGJvYXJkfGVufDF8fHx8MTc2MjE2NDkzMnww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      },
      {
        title: 'Digitale Transformation',
        category: 'Digitalisierung',
        description: 'Komplette Digitalisierung der Geschäftsprozesse eines mittelständischen Unternehmens.',
        results: [
          '40% Effizienzsteigerung',
          'Papierlose Workflows',
          'Cloud-basierte Zusammenarbeit',
        ],
        image: 'https://images.unsplash.com/photo-1644325349124-d1756b79dd42?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdHJhbnNmb3JtYXRpb258ZW58MXx8fHwxNzYyMDk4MzE5fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      },
      {
        title: 'Custom CRM System',
        category: 'Softwareentwicklung',
        description: 'Massgeschneidertes CRM-System mit KI-gestützter Kundenanalyse.',
        results: [
          '35% höhere Kundenbindung',
          'Automatische Lead-Qualifizierung',
          'Integration bestehender Tools',
        ],
        image: 'https://images.unsplash.com/photo-1630283017802-785b7aff9aac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBvZmZpY2UlMjB3b3Jrc3BhY2V8ZW58MXx8fHwxNzYyMDcxMzE0fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      },
    ],
  },
  en: {
    title: 'Case Studies',
    subtitle: 'Success stories of our clients',
    viewMore: 'Learn more',
    cases: [
      {
        title: 'Analytics Dashboard for SME',
        category: 'Data Analysis',
        description: 'Development of an intuitive dashboard for real-time monitoring of business metrics.',
        results: [
          '60% faster decision-making',
          'Automated reporting processes',
          'Increased data transparency',
        ],
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwYW5hbHl0aWNzJTIwZGFzaGJvYXJkfGVufDF8fHx8MTc2MjE2NDkzMnww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      },
      {
        title: 'Digital Transformation',
        category: 'Digitalization',
        description: 'Complete digitalization of business processes for a mid-sized company.',
        results: [
          '40% efficiency increase',
          'Paperless workflows',
          'Cloud-based collaboration',
        ],
        image: 'https://images.unsplash.com/photo-1644325349124-d1756b79dd42?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdHJhbnNmb3JtYXRpb258ZW58MXx8fHwxNzYyMDk4MzE5fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      },
      {
        title: 'Custom CRM System',
        category: 'Software Development',
        description: 'Tailor-made CRM system with AI-powered customer analysis.',
        results: [
          '35% higher customer retention',
          'Automatic lead qualification',
          'Integration of existing tools',
        ],
        image: 'https://images.unsplash.com/photo-1630283017802-785b7aff9aac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBvZmZpY2UlMjB3b3Jrc3BhY2V8ZW58MXx8fHwxNzYyMDcxMzE0fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      },
    ],
  },
};

export function CaseStudies({ language }: CaseStudiesProps) {
  const t = translations[language];

  return (
    <section id="cases" className="py-24 bg-secondary/50 scroll-mt-20">
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

        <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {t.cases.map((caseStudy, index) => (
            <motion.div
              key={caseStudy.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="bg-card border border-border rounded-2xl overflow-hidden group hover:border-primary/50 transition-all"
            >
              <div className="relative h-48 overflow-hidden">
                <ImageWithFallback
                  src={caseStudy.image}
                  alt={caseStudy.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute top-4 left-4">
                  <span className="px-3 py-1 bg-primary text-primary-foreground rounded-full text-sm">
                    {caseStudy.category}
                  </span>
                </div>
              </div>
              
              <div className="p-6">
                <h3 className="text-xl mb-3">{caseStudy.title}</h3>
                <p className="text-muted-foreground mb-6">{caseStudy.description}</p>
                
                <div className="space-y-2 mb-6">
                  {caseStudy.results.map((result) => (
                    <div key={result} className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-muted-foreground">{result}</span>
                    </div>
                  ))}
                </div>

                <button className="flex items-center gap-2 text-primary hover:gap-3 transition-all">
                  {t.viewMore}
                  <ArrowUpRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
