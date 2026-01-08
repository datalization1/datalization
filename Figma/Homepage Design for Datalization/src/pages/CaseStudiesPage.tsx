import { motion } from 'motion/react';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';
import { ArrowUpRight, CheckCircle, TrendingUp, Target, Users, Zap } from 'lucide-react';

interface CaseStudiesPageProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Case Studies',
    subtitle: 'Erfolgsgeschichten unserer Kunden - Von der Herausforderung zur Lösung',
    intro: 'Erfahren Sie, wie wir Unternehmen bei ihrer digitalen Transformation unterstützen und messbare Erfolge erzielen.',
    viewMore: 'Details ansehen',
    challenge: 'Herausforderung',
    solution: 'Lösung',
    results: 'Ergebnisse',
    impact: 'Impact',
    stats: [
      {
        icon: Users,
        value: '50+',
        label: 'Zufriedene Kunden',
      },
      {
        icon: Target,
        value: '100+',
        label: 'Erfolgreiche Projekte',
      },
      {
        icon: TrendingUp,
        value: '40%',
        label: 'Durchschn. Effizienzsteigerung',
      },
      {
        icon: Zap,
        value: '24h',
        label: 'Response Zeit',
      },
    ],
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
      {
        title: 'Supply Chain Optimierung',
        category: 'Beratung & Datenanalyse',
        client: 'Logistikunternehmen',
        description: 'Optimierung der Lieferkette durch datengetriebene Analysen und Prozessberatung.',
        challenge: 'Hohe Lagerkosten, ineffiziente Routenplanung und mangelnde Transparenz in der Lieferkette führten zu Wettbewerbsnachteilen.',
        solution: 'Umfassende Datenanalyse der Supply Chain, Implementierung von Predictive Analytics für Bedarfsplanung und Optimierung der Logistikprozesse durch strategische Beratung.',
        results: [
          'Reduktion der Lagerkosten um 28%',
          'Optimierte Routenplanung spart 15% Kraftstoff',
          'Lieferzeitverkürzung um 20%',
          'Echtzeit-Transparenz über die gesamte Lieferkette',
        ],
        image: 'https://images.unsplash.com/photo-1649478680984-01586ce84ac0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9qZWN0JTIwbWFuYWdlbWVudHxlbnwxfHx8fDE3Njc4MDU0MTR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['Python', 'Tableau', 'SAP Integration', 'Machine Learning'],
      },
      {
        title: 'Marketing Automation',
        category: 'Softwareentwicklung',
        client: 'B2B SaaS Startup',
        description: 'Automatisierung von Marketing-Prozessen mit intelligenter Kundensegmentierung.',
        challenge: 'Manuelles Marketing war zeitaufwendig und nicht skalierbar. Fehlende Segmentierung führte zu geringer Conversion.',
        solution: 'Entwicklung einer Marketing-Automation-Plattform mit KI-gestützter Segmentierung und personalisierten Kampagnen. Integration mit CRM und Analytics.',
        results: [
          '50% Zeitersparnis im Marketing-Team',
          'Conversion Rate Steigerung um 45%',
          'Automatische Segmentierung von 10.000+ Kontakten',
          'ROI-Steigerung von Marketing-Kampagnen um 60%',
        ],
        image: 'https://images.unsplash.com/photo-1744782211816-c5224434614f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwYW5hbHlzaXMlMjBjb21wdXRlcnxlbnwxfHx8fDE3Njc4NjkxNjl8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['TypeScript', 'Next.js', 'MongoDB', 'SendGrid'],
      },
      {
        title: 'Finanz-Reporting System',
        category: 'Digitalisierung',
        client: 'Finanzdienstleister',
        description: 'Automatisiertes Reporting-System für regulatorische Anforderungen.',
        challenge: 'Komplexe regulatorische Anforderungen erforderten zeitaufwendiges manuelles Reporting. Fehlerrisiko war hoch und Compliance schwer nachweisbar.',
        solution: 'Entwicklung eines automatisierten Reporting-Systems, das alle regulatorischen Anforderungen erfüllt. Automatische Datenvalidierung und Audit-Trail für vollständige Compliance.',
        results: [
          'Zeitersparnis von 80% beim Reporting',
          '100% Compliance mit allen Vorschriften',
          'Fehlerrate auf nahezu 0% reduziert',
          'Vollständige Audit-Trails für alle Berichte',
        ],
        image: 'https://images.unsplash.com/photo-1626105985445-6430a31f6f96?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMHN1Y2Nlc3MlMjBtZWV0aW5nfGVufDF8fHx8MTc2Nzg4Njk2NHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['C#', '.NET Core', 'SQL Server', 'Power BI'],
      },
    ],
  },
  en: {
    title: 'Case Studies',
    subtitle: 'Success Stories of Our Clients - From Challenge to Solution',
    intro: 'Discover how we support companies in their digital transformation and achieve measurable success.',
    viewMore: 'View Details',
    challenge: 'Challenge',
    solution: 'Solution',
    results: 'Results',
    impact: 'Impact',
    stats: [
      {
        icon: Users,
        value: '50+',
        label: 'Satisfied Clients',
      },
      {
        icon: Target,
        value: '100+',
        label: 'Successful Projects',
      },
      {
        icon: TrendingUp,
        value: '40%',
        label: 'Avg. Efficiency Increase',
      },
      {
        icon: Zap,
        value: '24h',
        label: 'Response Time',
      },
    ],
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
      {
        title: 'Supply Chain Optimization',
        category: 'Consulting & Data Analysis',
        client: 'Logistics Company',
        description: 'Supply chain optimization through data-driven analysis and process consulting.',
        challenge: 'High inventory costs, inefficient route planning, and lack of transparency in the supply chain led to competitive disadvantages.',
        solution: 'Comprehensive data analysis of the supply chain, implementation of predictive analytics for demand planning, and optimization of logistics processes through strategic consulting.',
        results: [
          '28% reduction in inventory costs',
          'Optimized route planning saves 15% fuel',
          '20% reduction in delivery time',
          'Real-time transparency across the entire supply chain',
        ],
        image: 'https://images.unsplash.com/photo-1649478680984-01586ce84ac0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9qZWN0JTIwbWFuYWdlbWVudHxlbnwxfHx8fDE3Njc4MDU0MTR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['Python', 'Tableau', 'SAP Integration', 'Machine Learning'],
      },
      {
        title: 'Marketing Automation',
        category: 'Software Development',
        client: 'B2B SaaS Startup',
        description: 'Automation of marketing processes with intelligent customer segmentation.',
        challenge: 'Manual marketing was time-consuming and not scalable. Lack of segmentation led to low conversion.',
        solution: 'Development of a marketing automation platform with AI-powered segmentation and personalized campaigns. Integration with CRM and analytics.',
        results: [
          '50% time savings in marketing team',
          '45% conversion rate increase',
          'Automatic segmentation of 10,000+ contacts',
          '60% ROI increase of marketing campaigns',
        ],
        image: 'https://images.unsplash.com/photo-1744782211816-c5224434614f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwYW5hbHlzaXMlMjBjb21wdXRlcnxlbnwxfHx8fDE3Njc4NjkxNjl8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['TypeScript', 'Next.js', 'MongoDB', 'SendGrid'],
      },
      {
        title: 'Financial Reporting System',
        category: 'Digitalization',
        client: 'Financial Services Provider',
        description: 'Automated reporting system for regulatory requirements.',
        challenge: 'Complex regulatory requirements required time-consuming manual reporting. Error risk was high and compliance difficult to prove.',
        solution: 'Development of an automated reporting system that meets all regulatory requirements. Automatic data validation and audit trail for complete compliance.',
        results: [
          '80% time savings in reporting',
          '100% compliance with all regulations',
          'Error rate reduced to nearly 0%',
          'Complete audit trails for all reports',
        ],
        image: 'https://images.unsplash.com/photo-1626105985445-6430a31f6f96?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMHN1Y2Nlc3MlMjBtZWV0aW5nfGVufDF8fHx8MTc2Nzg4Njk2NHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        technologies: ['C#', '.NET Core', 'SQL Server', 'Power BI'],
      },
    ],
  },
};

export function CaseStudiesPage({ language }: CaseStudiesPageProps) {
  const t = translations[language];

  return (
    <main className="min-h-screen pt-24">
      {/* Hero Section */}
      <section className="py-16 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-[#f7931a]/5 via-transparent to-transparent pointer-events-none" />
        
        <div className="container mx-auto px-4 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h1 className="text-5xl md:text-6xl mb-6">{t.title}</h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-4">{t.subtitle}</p>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">{t.intro}</p>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-5xl mx-auto mb-16"
          >
            {t.stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div
                  key={stat.label}
                  className="bg-card border border-border rounded-xl p-6 text-center"
                >
                  <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-6 h-6 text-primary" />
                  </div>
                  <div className="text-3xl font-bold text-primary mb-2">{stat.value}</div>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                </div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* Case Studies */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="space-y-16 max-w-7xl mx-auto">
            {t.cases.map((caseStudy, index) => (
              <motion.div
                key={caseStudy.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="bg-card border border-border rounded-2xl overflow-hidden"
              >
                <div className="grid lg:grid-cols-2 gap-8">
                  {/* Image */}
                  <div className="relative h-64 lg:h-auto overflow-hidden">
                    <ImageWithFallback
                      src={caseStudy.image}
                      alt={caseStudy.title}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="px-4 py-2 bg-primary text-primary-foreground rounded-full text-sm font-medium">
                        {caseStudy.category}
                      </span>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="p-8 lg:py-12">
                    <h2 className="text-3xl mb-2">{caseStudy.title}</h2>
                    <p className="text-muted-foreground text-sm mb-6">{caseStudy.client}</p>
                    <p className="text-lg mb-8">{caseStudy.description}</p>

                    {/* Challenge */}
                    <div className="mb-6">
                      <h3 className="text-lg font-semibold mb-2 text-primary">{t.challenge}</h3>
                      <p className="text-muted-foreground text-sm">{caseStudy.challenge}</p>
                    </div>

                    {/* Solution */}
                    <div className="mb-6">
                      <h3 className="text-lg font-semibold mb-2 text-primary">{t.solution}</h3>
                      <p className="text-muted-foreground text-sm">{caseStudy.solution}</p>
                    </div>

                    {/* Results */}
                    <div className="mb-6">
                      <h3 className="text-lg font-semibold mb-3 text-primary">{t.results}</h3>
                      <div className="space-y-2">
                        {caseStudy.results.map((result) => (
                          <div key={result} className="flex items-start gap-2">
                            <CheckCircle className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
                            <span className="text-sm text-muted-foreground">{result}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Technologies */}
                    <div className="flex flex-wrap gap-2">
                      {caseStudy.technologies.map((tech) => (
                        <span
                          key={tech}
                          className="px-3 py-1 bg-secondary border border-border rounded-full text-xs"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-zinc-900/50">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-2xl p-12 text-center max-w-4xl mx-auto"
          >
            <h2 className="text-3xl md:text-4xl mb-4">
              {language === 'de'
                ? 'Bereit für Ihre Erfolgsgeschichte?'
                : 'Ready for Your Success Story?'}
            </h2>
            <p className="text-muted-foreground mb-8 text-lg">
              {language === 'de'
                ? 'Lassen Sie uns gemeinsam Ihr nächstes Projekt zum Erfolg führen.'
                : 'Let\'s make your next project a success together.'}
            </p>
            <button className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium">
              {language === 'de' ? 'Jetzt Kontakt aufnehmen' : 'Contact Us Now'}
              <ArrowUpRight className="w-5 h-5" />
            </button>
          </motion.div>
        </div>
      </section>
    </main>
  );
}
