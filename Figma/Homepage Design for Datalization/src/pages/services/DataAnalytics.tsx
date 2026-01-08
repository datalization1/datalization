import { ServiceHero } from '../../components/service-details/ServiceHero';
import { QuickCheckButton } from '../../components/service-details/QuickCheckButton';
import { OutcomesSection } from '../../components/service-details/OutcomesSection';
import { ProcessSection } from '../../components/service-details/ProcessSection';
import { ExamplesSection } from '../../components/service-details/ExamplesSection';
import { DeliverablesSection } from '../../components/service-details/DeliverablesSection';
import { FAQSection } from '../../components/service-details/FAQSection';
import { CTASection } from '../../components/service-details/CTASection';
import { StickyCTA } from '../../components/service-details/StickyCTA';
import { Users, Target, TrendingUp, BarChart3, Database, FileText, GraduationCap, Settings, Utensils, Wrench, Shield } from 'lucide-react';
import { motion } from 'motion/react';
import { ImageWithFallback } from '../../components/figma/ImageWithFallback';

interface DataAnalyticsProps {
  language: 'de' | 'en';
  onContact: () => void;
  onNavigateToFinder?: () => void;
}

const content = {
  de: {
    hero: {
      headline: 'Aus Zahlen wird Klarheit',
      subline: 'Wir helfen KMUs, den Überblick zu gewinnen und aus Erfahrung zu lernen – verständlich, praxisnah und ohne Daten-Chaos.',
      primaryCTA: 'Kurz-Check buchen',
      secondaryCTA: 'Beispiel ansehen',
    },
    quickCheck: {
      title: 'Passt das zu Ihnen?',
      questions: [
        'Ich habe Zahlen, aber keinen Überblick',
        'Ich arbeite in Excel, aber es ist mühsam',
        'Wir wollen weniger manuelle Arbeit',
        'Wir möchten Prognosen/Planung verbessern',
        'Entscheidungen basieren zu oft auf Gefühl',
        'Wir wissen nicht, was wirklich profitabel ist',
      ],
      result: 'Datenanalyse & Data Science könnte genau das Richtige für Sie sein.',
      cta: 'Kostenlosen 20-Minuten Check buchen',
    },
    outcomes: {
      title: 'Was Sie am Ende haben',
      description: 'Konkrete Verbesserungen in Ihrem Alltag – nicht nur schöne Dashboards.',
      items: [
        'Überblick über Umsatz, Deckung und Zeitverläufe auf einen Blick',
        'Frühwarnsignale bei Abweichungen – bevor Probleme entstehen',
        'Entscheidungen weniger nach Gefühl, mehr nach Sichtbarkeit',
        'Planung wird ruhiger (Personal, Einkauf, Kapazitäten)',
        'Weniger Zeit mit Excel-Arbeit, mehr Zeit für strategische Fragen',
        'Fundierte Basis für Gespräche mit Bank, Partnern oder Investoren',
      ],
    },
    process: {
      title: 'So arbeiten wir',
      subtitle: 'Von der Herausforderung zur Lösung – in klaren Schritten',
      steps: [
        {
          icon: Users,
          title: 'Kennenlernen & Ziel klären',
          description: 'Wir verstehen Ihre Herausforderung: Was soll besser werden? Welche Fragen bleiben heute unbeantwortet?',
        },
        {
          icon: Database,
          title: 'Datenquellen verbinden',
          description: 'Wir sammeln Daten aus Kasse, Excel, ERP oder Buchhaltung – und bringen Struktur rein.',
        },
        {
          icon: Target,
          title: 'Struktur & KPIs definieren',
          description: 'Gemeinsam legen wir fest, welche Kennzahlen wirklich wichtig sind – verständlich und umsetzbar.',
        },
        {
          icon: BarChart3,
          title: 'Dashboard / Report bauen',
          description: 'Wir erstellen übersichtliche Visualisierungen, die Sie täglich nutzen können – ohne Schulung.',
        },
        {
          icon: TrendingUp,
          title: 'Prognosen & Automatisierung (Optional)',
          description: 'Data Science: Vorhersagen für Umsatz, Bedarf oder Risiken – damit Sie rechtzeitig planen können.',
        },
        {
          icon: GraduationCap,
          title: 'Übergabe & Schulung',
          description: 'Wir zeigen Ihnen, wie alles funktioniert – und bleiben Ansprechpartner für Fragen.',
        },
      ],
    },
    examples: {
      title: 'Beispiele aus der Praxis',
      subtitle: 'Branchen-neutrale Szenarien, die zeigen, was möglich ist',
      items: [
        {
          icon: Utensils,
          industry: 'Gastronomie',
          scenario: 'Mittag vs. Abend – welche Karte lohnt sich? Welche Gerichte bringen wirklich Marge?',
        },
        {
          icon: Wrench,
          industry: 'Handwerk',
          scenario: 'Welche Aufträge bringen echten Gewinn? Wo geht Zeit verloren?',
        },
        {
          icon: Shield,
          industry: 'Versicherung',
          scenario: 'Welche Fälle häufen sich? Wo lohnt sich Prävention statt Reaktion?',
        },
      ],
    },
    deliverables: {
      title: 'Was wir liefern',
      subtitle: 'Konkrete Ergebnisse, die Sie sofort nutzen können',
      items: [
        {
          icon: Target,
          title: 'KPI-Set + Definitionen',
          description: 'Klare Kennzahlen, die zu Ihrem Geschäft passen',
        },
        {
          icon: BarChart3,
          title: 'Dashboard (Power BI / Web)',
          description: 'Interaktive Visualisierung Ihrer Daten',
        },
        {
          icon: Settings,
          title: 'Report-Automation',
          description: 'Automatische Updates – keine manuelle Arbeit mehr',
        },
        {
          icon: Database,
          title: 'Datenmodell / Grundlage',
          description: 'Saubere Struktur für zukünftige Erweiterungen',
        },
        {
          icon: FileText,
          title: 'Dokumentation',
          description: 'Alles verständlich erklärt – für Sie und Ihr Team',
        },
        {
          icon: GraduationCap,
          title: 'Einführung & Support',
          description: 'Persönliche Schulung und laufende Unterstützung',
        },
      ],
    },
    faq: {
      title: 'Häufige Fragen',
      subtitle: 'Klarheit schaffen, bevor es losgeht',
      items: [
        {
          question: 'Muss ich neue Software kaufen?',
          answer: 'Nicht zwingend. Wir arbeiten mit dem, was Sie bereits haben. Falls nötig, empfehlen wir kosteneffiziente Lösungen wie Power BI (oft bereits in Microsoft 365 enthalten) oder Web-basierte Dashboards.',
        },
        {
          question: 'Was, wenn meine Daten unvollständig sind?',
          answer: 'Das ist häufig der Fall. Wir helfen, die vorhandenen Daten zu strukturieren und zeigen, wo Lücken sind. Oft lässt sich schon mit 70% der Daten viel Klarheit schaffen.',
        },
        {
          question: 'Kann ich klein starten?',
          answer: 'Absolut. Wir empfehlen oft, mit 2-3 wichtigen Kennzahlen zu beginnen. Sobald diese Mehrwert bringen, können wir erweitern.',
        },
        {
          question: 'Wer sieht meine Daten?',
          answer: 'Nur Sie und die Personen, die Sie berechtigen. Wir arbeiten mit höchster Vertraulichkeit und können bei Bedarf NDAs unterschreiben.',
        },
        {
          question: 'Wie schnell sehe ich erste Ergebnisse?',
          answer: 'Oft können wir innerhalb von 2-4 Wochen ein erstes Dashboard zeigen. Komplexere Analysen oder Prognosemodelle brauchen etwas länger.',
        },
        {
          question: 'Ist das ein Grossprojekt?',
          answer: 'Nein. Die meisten unserer Projekte starten klein und pragmatisch. Wir bauen Schritt für Schritt – kein Big Bang, keine Monats-Projekte ohne Zwischenergebnisse.',
        },
        {
          question: 'Was kostet das?',
          answer: 'Das hängt vom Umfang ab. Ein einfaches Dashboard kann bei wenigen Tausend Franken starten. Wir erstellen nach dem Erstgespräch eine transparente Kostenschätzung.',
        },
        {
          question: 'Brauche ich technisches Wissen?',
          answer: 'Nein. Wir erklären alles verständlich und bauen Lösungen, die Sie ohne IT-Studium nutzen können.',
        },
      ],
    },
    cta: {
      title: 'Bereit für mehr Klarheit?',
      description: 'Buchen Sie einen kostenlosen 20-Minuten Check. Wir schauen gemeinsam, ob und wie Datenanalyse Ihnen helfen kann.',
      primaryCTA: 'Jetzt Check buchen',
      secondaryCTA: 'Kontakt aufnehmen',
      downloadPDF: 'Datenanalyse & Data Science – Kompakt erklärt (PDF)',
    },
    stickyCTA: 'Kurz-Check buchen',
  },
  en: {
    hero: {
      headline: 'From Numbers to Clarity',
      subline: 'We help SMEs gain overview and learn from experience – understandable, practical, and without data chaos.',
      primaryCTA: 'Book Quick Check',
      secondaryCTA: 'View Example',
    },
    quickCheck: {
      title: 'Is This Right for You?',
      questions: [
        'I have numbers, but no overview',
        'I work in Excel, but it\'s cumbersome',
        'We want less manual work',
        'We want to improve forecasts/planning',
        'Decisions are too often based on gut feeling',
        'We don\'t know what\'s really profitable',
      ],
      result: 'Data Analytics & Data Science could be exactly right for you.',
      cta: 'Book Free 20-Minute Check',
    },
    outcomes: {
      title: 'What You Get',
      description: 'Concrete improvements in your daily work – not just pretty dashboards.',
      items: [
        'Overview of revenue, margins, and trends at a glance',
        'Early warning signals for deviations – before problems arise',
        'Decisions less by feeling, more by visibility',
        'Planning becomes calmer (staff, purchasing, capacity)',
        'Less time with Excel work, more time for strategic questions',
        'Solid foundation for conversations with banks, partners, or investors',
      ],
    },
    process: {
      title: 'How We Work',
      subtitle: 'From challenge to solution – in clear steps',
      steps: [
        {
          icon: Users,
          title: 'Get to Know & Define Goal',
          description: 'We understand your challenge: What should improve? Which questions remain unanswered today?',
        },
        {
          icon: Database,
          title: 'Connect Data Sources',
          description: 'We collect data from POS, Excel, ERP, or accounting – and bring structure.',
        },
        {
          icon: Target,
          title: 'Define Structure & KPIs',
          description: 'Together we determine which metrics really matter – understandable and actionable.',
        },
        {
          icon: BarChart3,
          title: 'Build Dashboard / Report',
          description: 'We create clear visualizations you can use daily – without training.',
        },
        {
          icon: TrendingUp,
          title: 'Forecasts & Automation (Optional)',
          description: 'Data Science: Predictions for revenue, demand, or risks – so you can plan ahead.',
        },
        {
          icon: GraduationCap,
          title: 'Handover & Training',
          description: 'We show you how everything works – and remain your contact for questions.',
        },
      ],
    },
    examples: {
      title: 'Examples from Practice',
      subtitle: 'Industry-neutral scenarios showing what\'s possible',
      items: [
        {
          icon: Utensils,
          industry: 'Gastronomy',
          scenario: 'Lunch vs. dinner – which menu is worthwhile? Which dishes really bring margin?',
        },
        {
          icon: Wrench,
          industry: 'Crafts',
          scenario: 'Which orders bring real profit? Where is time being lost?',
        },
        {
          icon: Shield,
          industry: 'Insurance',
          scenario: 'Which cases are accumulating? Where is prevention better than reaction?',
        },
      ],
    },
    deliverables: {
      title: 'What We Deliver',
      subtitle: 'Concrete results you can use immediately',
      items: [
        {
          icon: Target,
          title: 'KPI Set + Definitions',
          description: 'Clear metrics that fit your business',
        },
        {
          icon: BarChart3,
          title: 'Dashboard (Power BI / Web)',
          description: 'Interactive visualization of your data',
        },
        {
          icon: Settings,
          title: 'Report Automation',
          description: 'Automatic updates – no more manual work',
        },
        {
          icon: Database,
          title: 'Data Model / Foundation',
          description: 'Clean structure for future expansions',
        },
        {
          icon: FileText,
          title: 'Documentation',
          description: 'Everything explained clearly – for you and your team',
        },
        {
          icon: GraduationCap,
          title: 'Introduction & Support',
          description: 'Personal training and ongoing assistance',
        },
      ],
    },
    faq: {
      title: 'Frequently Asked Questions',
      subtitle: 'Creating clarity before we start',
      items: [
        {
          question: 'Do I need to buy new software?',
          answer: 'Not necessarily. We work with what you already have. If needed, we recommend cost-effective solutions like Power BI (often already included in Microsoft 365) or web-based dashboards.',
        },
        {
          question: 'What if my data is incomplete?',
          answer: 'That\'s often the case. We help structure the available data and show where gaps are. Often, much clarity can be created with 70% of the data.',
        },
        {
          question: 'Can I start small?',
          answer: 'Absolutely. We often recommend starting with 2-3 important metrics. Once these bring value, we can expand.',
        },
        {
          question: 'Who sees my data?',
          answer: 'Only you and the people you authorize. We work with the highest confidentiality and can sign NDAs if needed.',
        },
        {
          question: 'How quickly will I see results?',
          answer: 'Often we can show a first dashboard within 2-4 weeks. More complex analyses or forecasting models take a bit longer.',
        },
        {
          question: 'Is this a big project?',
          answer: 'No. Most of our projects start small and pragmatic. We build step by step – no big bang, no month-long projects without intermediate results.',
        },
        {
          question: 'What does it cost?',
          answer: 'It depends on the scope. A simple dashboard can start at a few thousand francs. We create a transparent cost estimate after the initial conversation.',
        },
        {
          question: 'Do I need technical knowledge?',
          answer: 'No. We explain everything clearly and build solutions you can use without an IT degree.',
        },
      ],
    },
    cta: {
      title: 'Ready for More Clarity?',
      description: 'Book a free 20-minute check. We\'ll look together at whether and how data analytics can help you.',
      primaryCTA: 'Book Check Now',
      secondaryCTA: 'Get in Touch',
      downloadPDF: 'Data Analytics & Data Science – Explained Simply (PDF)',
    },
    stickyCTA: 'Book Quick Check',
  },
};

export function DataAnalytics({ language, onContact, onNavigateToFinder }: DataAnalyticsProps) {
  const t = content[language];

  // Hero Visual - Dashboard Animation
  const DashboardVisual = () => (
    <div className="relative">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8 }}
        className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl overflow-hidden shadow-2xl"
      >
        {/* Fixed height container matching other services */}
        <div className="relative h-[400px]">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkYXRhJTIwYW5hbHl0aWNzJTIwZGFzaGJvYXJkfGVufDF8fHx8MTc2Nzg1MTMwM3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
            alt="Data Analytics Dashboard"
            className="w-full h-full object-cover"
          />
          {/* Overlay with analytics features */}
          <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-zinc-950/50 to-transparent flex items-end p-6">
            <div className="space-y-2">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <BarChart3 className="w-4 h-4 text-[#f7931a]" />
                <span>Real-time KPIs</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <TrendingUp className="w-4 h-4 text-[#f7931a]" />
                <span>Predictive Analytics</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Target className="w-4 h-4 text-[#f7931a]" />
                <span>Actionable Insights</span>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );

  // Outcomes Visual - Before/After
  const OutcomesVisual = () => (
    <div className="space-y-4">
      {/* Before */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
        className="bg-zinc-900/30 border border-zinc-800 rounded-xl p-6"
      >
        <div className="text-sm text-zinc-500 mb-3">Vorher</div>
        <div className="space-y-2 opacity-60">
          <div className="h-3 bg-zinc-800 rounded w-3/4"></div>
          <div className="h-3 bg-zinc-800 rounded w-full"></div>
          <div className="h-3 bg-zinc-800 rounded w-2/3"></div>
        </div>
        <div className="text-xs text-zinc-600 mt-3">Excel-Chaos, keine Übersicht</div>
      </motion.div>

      {/* After */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2 }}
        className="bg-[#f7931a]/10 border border-[#f7931a]/30 rounded-xl p-6"
      >
        <div className="text-sm text-[#f7931a] mb-3">Nachher</div>
        <div className="space-y-2">
          <div className="h-3 bg-[#f7931a]/30 rounded w-full"></div>
          <div className="h-3 bg-[#f7931a]/20 rounded w-5/6"></div>
          <div className="h-3 bg-[#f7931a]/20 rounded w-4/5"></div>
        </div>
        <div className="text-xs text-[#f7931a] mt-3">Klare Kennzahlen, sofort verfügbar</div>
      </motion.div>
    </div>
  );

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <ServiceHero
        headline={t.hero.headline}
        subline={t.hero.subline}
        primaryCTAText={t.hero.primaryCTA}
        secondaryCTAText={t.hero.secondaryCTA}
        onPrimaryCTA={onContact}
        onSecondaryCTA={() => {
          document.getElementById('examples')?.scrollIntoView({ behavior: 'smooth' });
        }}
        visual={<DashboardVisual />}
      />

      <QuickCheckButton
        language={language}
        onNavigate={onNavigateToFinder || (() => {})}
      />

      <OutcomesSection
        title={t.outcomes.title}
        description={t.outcomes.description}
        outcomes={t.outcomes.items}
        visual={<OutcomesVisual />}
      />

      <ProcessSection
        title={t.process.title}
        subtitle={t.process.subtitle}
        steps={t.process.steps}
      />

      <div id="examples">
        <ExamplesSection
          title={t.examples.title}
          subtitle={t.examples.subtitle}
          examples={t.examples.items}
        />
      </div>

      <DeliverablesSection
        title={t.deliverables.title}
        subtitle={t.deliverables.subtitle}
        deliverables={t.deliverables.items}
      />

      <FAQSection
        title={t.faq.title}
        subtitle={t.faq.subtitle}
        faqs={t.faq.items}
      />

      <CTASection
        title={t.cta.title}
        description={t.cta.description}
        primaryCTA={{
          text: t.cta.primaryCTA,
          onClick: onContact,
        }}
        secondaryCTA={{
          text: t.cta.secondaryCTA,
          onClick: onContact,
        }}
        downloadPDF={{
          text: t.cta.downloadPDF,
          filename: 'datalization-datenanalyse.pdf',
        }}
      />

      <StickyCTA text={t.stickyCTA} onClick={onContact} />
    </div>
  );
}