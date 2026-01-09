import { motion } from 'motion/react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { ArrowUpRight, CheckCircle, X } from 'lucide-react';
import { useState } from 'react';

interface CaseStudiesProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Case Studies',
    subtitle: 'Erfolgsgeschichten unserer Kunden',
    viewMore: 'Mehr erfahren',
    close: 'Schließen',
    challenge: 'Herausforderung',
    solution: 'Lösung',
    results: 'Ergebnisse',
    technologies: 'Technologien',
    cases: [
      {
        title: 'Analytics Dashboard für KMU',
        category: 'Datenanalyse',
        client: 'Mittelständisches Produktionsunternehmen',
        description: 'Entwicklung eines intuitiven Dashboards zur Echtzeitüberwachung von Geschäftskennzahlen.',
        challenge: 'Das Unternehmen hatte keine zentrale Übersicht über wichtige Geschäftskennzahlen. Daten waren in verschiedenen Systemen verstreut und Reporting war zeitaufwendig und fehleranfällig.',
        solution: 'Wir entwickelten ein massgeschneidertes Analytics Dashboard, das alle relevanten Datenquellen integriert und in Echtzeit visualisiert. Automatisierte Berichte und KI-gestützte Insights ermöglichen schnellere Entscheidungen.',
        results: [
          '60% schnellere Entscheidungsfindung',
          'Automatisierte Reporting-Prozesse',
          'Erhöhte Datentransparenz im gesamten Unternehmen',
          'Reduktion manueller Dateneingabe um 75%',
        ],
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwYW5hbHl0aWNzJTIwZGFzaGJvYXJkfGVufDF8fHx8MTc2MjE2NDkzMnww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['Python', 'Power BI', 'Azure', 'SQL'],
      },
      {
        title: 'Digitale Transformation',
        category: 'Digitalisierung',
        client: 'Schweizer Beratungsunternehmen',
        description: 'Komplette Digitalisierung der Geschäftsprozesse eines mittelständischen Unternehmens.',
        challenge: 'Papierbasierte Prozesse führten zu Ineffizienzen, langen Bearbeitungszeiten und erschwerter Remote-Arbeit. Die bestehende IT-Infrastruktur war veraltet und nicht cloudbasiert.',
        solution: 'Umfassende Digitalisierung aller Kernprozesse mit cloudbasierten Lösungen. Implementierung von digitalen Workflows, Dokumentenmanagement und kollaborativen Tools. Schulung der Mitarbeiter für die neue digitale Arbeitsweise.',
        results: [
          '40% Effizienzsteigerung in den Kernprozessen',
          'Papierlose Workflows für alle Abteilungen',
          'Cloud-basierte Zusammenarbeit ermöglicht',
          'Kosteneinsparung von 30% durch Prozessoptimierung',
        ],
        image: 'https://images.unsplash.com/photo-1644325349124-d1756b79dd42?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdHJhbnNmb3JtYXRpb258ZW58MXx8fHwxNzYyMDk4MzE5fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['Microsoft 365', 'SharePoint', 'Power Automate', 'Teams'],
      },
      {
        title: 'Custom CRM System',
        category: 'Softwareentwicklung',
        client: 'E-Commerce Unternehmen',
        description: 'Massgeschneidertes CRM-System mit KI-gestützter Kundenanalyse.',
        challenge: 'Standardlösungen erfüllten nicht die spezifischen Anforderungen. Kundendaten waren fragmentiert und es fehlte eine intelligente Analyse für personalisierte Kundenbetreuung.',
        solution: 'Entwicklung eines maßgeschneiderten CRM-Systems mit KI-Komponenten für Kundenanalyse und Predictive Analytics. Integration aller bestehenden Tools und automatisierte Lead-Qualifizierung.',
        results: [
          '35% höhere Kundenbindung',
          'Automatische Lead-Qualifizierung spart 20h/Woche',
          'Integration aller bestehenden Tools',
          'Personalisierte Kundenansprache steigert Conversion um 25%',
        ],
        image: 'https://images.unsplash.com/photo-1630283017802-785b7aff9aac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBvZmZpY2UlMjB3b3Jrc3BhY2V8ZW58MXx8fHwxNzYyMDcxMzE0fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['React', 'Node.js', 'PostgreSQL', 'TensorFlow'],
      },
    ],
  },
  en: {
    title: 'Case Studies',
    subtitle: 'Success stories of our clients',
    viewMore: 'Learn more',
    close: 'Close',
    challenge: 'Challenge',
    solution: 'Solution',
    results: 'Results',
    technologies: 'Technologies',
    cases: [
      {
        title: 'Analytics Dashboard for SME',
        category: 'Data Analysis',
        client: 'Mid-sized Manufacturing Company',
        description: 'Development of an intuitive dashboard for real-time monitoring of business metrics.',
        challenge: 'The company had no central overview of important business metrics. Data was scattered across different systems and reporting was time-consuming and error-prone.',
        solution: 'We developed a customized analytics dashboard that integrates all relevant data sources and visualizes them in real-time. Automated reports and AI-powered insights enable faster decisions.',
        results: [
          '60% faster decision-making',
          'Automated reporting processes',
          'Increased data transparency throughout the company',
          '75% reduction in manual data entry',
        ],
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwYW5hbHl0aWNzJTIwZGFzaGJvYXJkfGVufDF8fHx8MTc2MjE2NDkzMnww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['Python', 'Power BI', 'Azure', 'SQL'],
      },
      {
        title: 'Digital Transformation',
        category: 'Digitalization',
        client: 'Swiss Consulting Firm',
        description: 'Complete digitalization of business processes for a mid-sized company.',
        challenge: 'Paper-based processes led to inefficiencies, long processing times, and difficult remote work. The existing IT infrastructure was outdated and not cloud-based.',
        solution: 'Comprehensive digitalization of all core processes with cloud-based solutions. Implementation of digital workflows, document management, and collaborative tools. Training of employees for the new digital way of working.',
        results: [
          '40% efficiency increase in core processes',
          'Paperless workflows for all departments',
          'Cloud-based collaboration enabled',
          '30% cost savings through process optimization',
        ],
        image: 'https://images.unsplash.com/photo-1644325349124-d1756b79dd42?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdHJhbnNmb3JtYXRpb258ZW58MXx8fHwxNzYyMDk4MzE5fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['Microsoft 365', 'SharePoint', 'Power Automate', 'Teams'],
      },
      {
        title: 'Custom CRM System',
        category: 'Software Development',
        client: 'E-Commerce Company',
        description: 'Tailor-made CRM system with AI-powered customer analysis.',
        challenge: 'Standard solutions did not meet specific requirements. Customer data was fragmented and intelligent analysis for personalized customer care was missing.',
        solution: 'Development of a customized CRM system with AI components for customer analysis and predictive analytics. Integration of all existing tools and automated lead qualification.',
        results: [
          '35% higher customer retention',
          'Automatic lead qualification saves 20h/week',
          'Integration of all existing tools',
          'Personalized customer approach increases conversion by 25%',
        ],
        image: 'https://images.unsplash.com/photo-1630283017802-785b7aff9aac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBvZmZpY2UlMjB3b3Jrc3BhY2V8ZW58MXx8fHwxNzYyMDcxMzE0fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['React', 'Node.js', 'PostgreSQL', 'TensorFlow'],
      },
    ],
  },
};

export function CaseStudies({ language }: CaseStudiesProps) {
  const t = translations[language];
  const [selectedCase, setSelectedCase] = useState<number | null>(null);

  return (
    <>
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
                className="bg-card border border-border rounded-2xl overflow-hidden group hover:border-primary/50 transition-all cursor-pointer"
                onClick={() => setSelectedCase(index)}
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
                  <p className="text-muted-foreground mb-6 line-clamp-2">{caseStudy.description}</p>
                  
                  <div className="space-y-2 mb-6">
                    {caseStudy.results.slice(0, 3).map((result) => (
                      <div key={result} className="flex items-start gap-2">
                        <CheckCircle className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-muted-foreground line-clamp-1">{result}</span>
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

      {/* Modal */}
      {selectedCase !== null && (
        <div 
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => setSelectedCase(null)}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-card border border-border rounded-2xl max-w-4xl w-full my-8 relative"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={() => setSelectedCase(null)}
              className="absolute top-4 right-4 z-10 w-10 h-10 bg-zinc-900/90 hover:bg-zinc-800 rounded-full flex items-center justify-center transition-colors"
            >
              <X className="w-5 h-5 text-white" />
            </button>

            {/* Modal Content */}
            <div className="relative">
              {/* Image */}
              <div className="relative h-64 overflow-hidden rounded-t-2xl">
                <ImageWithFallback
                  src={t.cases[selectedCase].image}
                  alt={t.cases[selectedCase].title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-4 left-4">
                  <span className="px-4 py-2 bg-primary text-primary-foreground rounded-full text-sm font-medium">
                    {t.cases[selectedCase].category}
                  </span>
                </div>
              </div>

              {/* Content */}
              <div className="p-8">
                <h2 className="text-3xl md:text-4xl mb-2">{t.cases[selectedCase].title}</h2>
                <p className="text-muted-foreground mb-6">{t.cases[selectedCase].client}</p>
                <p className="text-lg mb-8">{t.cases[selectedCase].description}</p>

                {/* Challenge */}
                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-3 text-primary flex items-center gap-2">
                    {t.challenge}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">{t.cases[selectedCase].challenge}</p>
                </div>

                {/* Solution */}
                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-3 text-primary flex items-center gap-2">
                    {t.solution}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">{t.cases[selectedCase].solution}</p>
                </div>

                {/* Results */}
                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-4 text-primary flex items-center gap-2">
                    {t.results}
                  </h3>
                  <div className="grid sm:grid-cols-2 gap-3">
                    {t.cases[selectedCase].results.map((result) => (
                      <div key={result} className="flex items-start gap-3 bg-secondary/50 p-3 rounded-lg">
                        <CheckCircle className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
                        <span className="text-sm">{result}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Technologies */}
                <div>
                  <h3 className="text-xl font-semibold mb-3 text-primary">{t.technologies}</h3>
                  <div className="flex flex-wrap gap-2">
                    {t.cases[selectedCase].technologies.map((tech) => (
                      <span
                        key={tech}
                        className="px-4 py-2 bg-primary/10 border border-primary/20 rounded-full text-sm font-medium"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </>
  );
}