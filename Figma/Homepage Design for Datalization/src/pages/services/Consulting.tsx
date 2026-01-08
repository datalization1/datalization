import { ServiceHero } from '../../components/service-details/ServiceHero';
import { QuickCheckButton } from '../../components/service-details/QuickCheckButton';
import { OutcomesSection } from '../../components/service-details/OutcomesSection';
import { ProcessSection } from '../../components/service-details/ProcessSection';
import { ExamplesSection } from '../../components/service-details/ExamplesSection';
import { DeliverablesSection } from '../../components/service-details/DeliverablesSection';
import { FAQSection } from '../../components/service-details/FAQSection';
import { CTASection } from '../../components/service-details/CTASection';
import { StickyCTA } from '../../components/service-details/StickyCTA';
import { Search, Lightbulb, Map, Settings, Compass, Target, TrendingUp, FileText, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { ImageWithFallback } from '../../components/figma/ImageWithFallback';

interface ConsultingProps {
  language: 'de' | 'en';
  onContact: () => void;
  onNavigateToFinder?: () => void;
}

const content = {
  de: {
    hero: {
      headline: 'Klarheit schaffen, richtig priorisieren',
      subline: 'Wir helfen Ihnen, den richtigen Weg zu finden – ohne Buzzwords, ohne teure Umwege.',
      primaryCTA: 'Kurz-Check buchen',
      secondaryCTA: 'Beispiel ansehen',
    },
    quickCheck: {
      title: 'Passt das zu Ihnen?',
      questions: [
        'Wir wissen nicht, wo wir anfangen sollen',
        'Wir haben viele Ideen, aber keine Priorisierung',
        'Technologie-Entscheidungen überfordern uns',
        'Wir wollen nicht in die falsche Lösung investieren',
        'Unser Team ist sich uneinig über die Richtung',
        'Wir brauchen eine realistische Roadmap',
      ],
      result: 'Beratung & Strategie könnte genau das Richtige für Sie sein.',
      cta: 'Kostenlosen 20-Minuten Check buchen',
    },
    outcomes: {
      title: 'Was Sie am Ende haben',
      description: 'Klarheit, Struktur und ein Fahrplan für Ihre digitale Zukunft.',
      items: [
        'Eine klare Datenstrategie – abgestimmt auf Ihre Geschäftsziele',
        'Priorisierte Roadmap mit realistischen Meilensteinen',
        'Technologie-Empfehlungen mit Kosten-Nutzen-Bewertung',
        'Risiko-Analyse und Vermeidung teurer Fehlentscheidungen',
        'Alignment im Team durch strukturierte Workshops',
        'Entscheidungsgrundlagen für Geschäftsführung und Stakeholder',
      ],
    },
    process: {
      title: 'Wie wir vorgehen',
      subtitle: 'Strukturiert, pragmatisch und auf Ihre Realität abgestimmt.',
      steps: [
        {
          icon: Search,
          title: 'Standortbestimmung',
          description: 'Wir analysieren Ihre aktuelle Situation, Ziele und Herausforderungen',
        },
        {
          icon: Lightbulb,
          title: 'Strategieentwicklung',
          description: 'Workshops und Konzeptarbeit mit Ihrem Team – mit klaren Ergebnissen',
        },
        {
          icon: Map,
          title: 'Roadmap & Empfehlungen',
          description: 'Priorisierte Maßnahmen, Technologie-Auswahl und Ressourcenplanung',
        },
        {
          icon: Settings,
          title: 'Umsetzungsbegleitung',
          description: 'Optional: Wir unterstützen bei der Implementierung oder Review',
        },
      ],
    },
    examples: {
      title: 'Typische Projekte',
      subtitle: 'Strategische Beratung in verschiedenen Bereichen',
      items: [
        {
          icon: Compass,
          industry: 'Datenstrategie-Entwicklung',
          scenario: 'Wie nutzen wir Daten, um bessere Entscheidungen zu treffen?',
        },
        {
          icon: Target,
          industry: 'Digitalisierungs-Roadmap',
          scenario: 'Welche Prozesse digitalisieren wir wann – und warum?',
        },
        {
          icon: TrendingUp,
          industry: 'Tool-Evaluierung',
          scenario: 'Welche Software passt zu uns? Make-or-Buy Entscheidungen.',
        },
      ],
    },
    deliverables: {
      title: 'Was Sie konkret erhalten',
      subtitle: 'Klare Empfehlungen und umsetzbare Pläne',
      items: [
        { icon: FileText, title: 'Strategiedokument mit klaren Empfehlungen', description: 'Strukturiert und praxisnah' },
        { icon: Map, title: 'Priorisierte Roadmap mit Zeitplan und Meilensteinen', description: 'Realistisch und umsetzbar' },
        { icon: CheckCircle, title: 'Technologie-Bewertung und Empfehlungen', description: 'Objektiv und transparent' },
        { icon: TrendingUp, title: 'Kosten-Nutzen-Analyse und ROI-Schätzungen', description: 'Für informierte Entscheidungen' },
        { icon: Lightbulb, title: 'Workshop-Ergebnisse und Alignment im Team', description: 'Alle ziehen am gleichen Strang' },
        { icon: Compass, title: 'Entscheidungsgrundlagen für Geschäftsführung', description: 'Klar und nachvollziehbar' },
      ],
    },
    faq: {
      title: 'Häufige Fragen',
      subtitle: 'Antworten auf die wichtigsten Fragen',
      items: [
        {
          question: 'Wie lange dauert ein Strategieprojekt?',
          answer: 'Typischerweise 4–8 Wochen, je nach Komplexität. Für eine erste Standortbestimmung reichen oft schon 2–3 Sitzungen.',
        },
        {
          question: 'Was kostet eine Strategieberatung?',
          answer: 'Die Kosten hängen vom Umfang ab. Eine kompakte Standortbestimmung startet bei CHF 3\'000–5\'000, umfassende Strategieprojekte bei CHF 10\'000+. Wir erstellen ein transparentes Angebot.',
        },
        {
          question: 'Brauchen wir danach noch weitere Unterstützung?',
          answer: 'Das entscheiden Sie. Wir können die Umsetzung begleiten, als Sparringspartner dienen oder Sie arbeiten die Roadmap selbst ab.',
        },
        {
          question: 'Was unterscheidet Sie von klassischen Unternehmensberatungen?',
          answer: 'Wir kennen die Praxis. Wir setzen selbst um, entwickeln Software und digitalisieren Prozesse – das macht unsere Empfehlungen realistisch und pragmatisch.',
        },
        {
          question: 'Können Sie auch bei der Umsetzung helfen?',
          answer: 'Ja, wir bieten das komplette Spektrum: Von der Strategie über die Entwicklung bis zur Digitalisierung. So bleibt alles aus einer Hand.',
        },
      ],
    },
    cta: {
      title: 'Bereit für strategische Klarheit?',
      description: 'Buchen Sie einen kostenlosen 20-Minuten Check. Wir besprechen Ihre Situation und zeigen auf, wie eine klare Strategie Ihnen Sicherheit und Fokus gibt.',
      primaryButton: 'Check buchen',
      secondaryButton: 'Oder schreiben Sie uns',
    },
    stickyCTA: {
      text: 'Mehr erfahren?',
      button: 'Check buchen',
    },
  },
  en: {
    hero: {
      headline: 'Create clarity, set priorities',
      subline: 'We help you find the right path – no buzzwords, no expensive detours.',
      primaryCTA: 'Book Quick Check',
      secondaryCTA: 'See Example',
    },
    quickCheck: {
      title: 'Is this right for you?',
      questions: [
        'We don\'t know where to start',
        'We have many ideas but no prioritization',
        'Technology decisions overwhelm us',
        'We don\'t want to invest in the wrong solution',
        'Our team disagrees about direction',
        'We need a realistic roadmap',
      ],
      result: 'Consulting & Strategy could be exactly what you need.',
      cta: 'Book Free 20-Minute Check',
    },
    outcomes: {
      title: 'What you\'ll have in the end',
      description: 'Clarity, structure, and a roadmap for your digital future.',
      items: [
        'A clear data strategy – aligned with your business goals',
        'Prioritized roadmap with realistic milestones',
        'Technology recommendations with cost-benefit analysis',
        'Risk analysis and avoidance of expensive mistakes',
        'Team alignment through structured workshops',
        'Decision basis for management and stakeholders',
      ],
    },
    process: {
      title: 'Our Approach',
      subtitle: 'Structured, pragmatic, and tailored to your reality.',
      steps: [
        {
          icon: Search,
          title: 'Assessment',
          description: 'We analyze your current situation, goals, and challenges',
        },
        {
          icon: Lightbulb,
          title: 'Strategy Development',
          description: 'Workshops and concept work with your team – with clear results',
        },
        {
          icon: Map,
          title: 'Roadmap & Recommendations',
          description: 'Prioritized actions, technology selection, and resource planning',
        },
        {
          icon: Settings,
          title: 'Implementation Support',
          description: 'Optional: We support during implementation or review',
        },
      ],
    },
    examples: {
      title: 'Typical Projects',
      subtitle: 'Strategic consulting in various areas',
      items: [
        {
          icon: Compass,
          industry: 'Data Strategy Development',
          scenario: 'How do we use data to make better decisions?',
        },
        {
          icon: Target,
          industry: 'Digitalization Roadmap',
          scenario: 'Which processes to digitalize when – and why?',
        },
        {
          icon: TrendingUp,
          industry: 'Tool Evaluation',
          scenario: 'Which software fits us? Make-or-buy decisions.',
        },
      ],
    },
    deliverables: {
      title: 'What you\'ll receive',
      subtitle: 'Clear recommendations and actionable plans',
      items: [
        { icon: FileText, title: 'Strategy document with clear recommendations', description: 'Structured and practical' },
        { icon: Map, title: 'Prioritized roadmap with timeline and milestones', description: 'Realistic and actionable' },
        { icon: CheckCircle, title: 'Technology assessment and recommendations', description: 'Objective and transparent' },
        { icon: TrendingUp, title: 'Cost-benefit analysis and ROI estimates', description: 'For informed decisions' },
        { icon: Lightbulb, title: 'Workshop results and team alignment', description: 'Everyone pulling in the same direction' },
        { icon: Compass, title: 'Decision basis for management', description: 'Clear and comprehensible' },
      ],
    },
    faq: {
      title: 'Frequently Asked Questions',
      subtitle: 'Answers to the most important questions',
      items: [
        {
          question: 'How long does a strategy project take?',
          answer: 'Typically 4–8 weeks, depending on complexity. For an initial assessment, 2–3 sessions are often enough.',
        },
        {
          question: 'What does strategy consulting cost?',
          answer: 'Costs depend on scope. A compact assessment starts at CHF 3,000–5,000, comprehensive strategy projects at CHF 10,000+. We create a transparent quote.',
        },
        {
          question: 'Do we need further support afterward?',
          answer: 'You decide. We can support implementation, serve as sparring partner, or you work through the roadmap yourself.',
        },
        {
          question: 'What sets you apart from traditional consulting firms?',
          answer: 'We know practice. We implement ourselves, develop software, and digitalize processes – that makes our recommendations realistic and pragmatic.',
        },
        {
          question: 'Can you also help with implementation?',
          answer: 'Yes, we offer the full spectrum: From strategy through development to digitalization. Everything from one source.',
        },
      ],
    },
    cta: {
      title: 'Ready for strategic clarity?',
      description: 'Book a free 20-minute check. We\'ll discuss your situation and show how a clear strategy gives you confidence and focus.',
      primaryButton: 'Book Check',
      secondaryButton: 'Or write to us',
    },
    stickyCTA: {
      text: 'Learn more?',
      button: 'Book Check',
    },
  },
};

export function Consulting({ language, onContact, onNavigateToFinder }: ConsultingProps) {
  const t = content[language];

  // Hero Visual - Strategy & Consulting
  const ConsultingVisual = () => (
    <div className="relative">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8 }}
        className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl overflow-hidden shadow-2xl"
      >
        {/* Fixed height container matching DataAnalytics */}
        <div className="relative h-[400px]">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1758691736084-4ef3e6f6a2cf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMGNvbnN1bHRpbmclMjBzdHJhdGVneXxlbnwxfHx8fDE3Njc4ODgwMjZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
            alt="Business Consulting & Strategy"
            className="w-full h-full object-cover"
          />
          {/* Overlay with strategy icons */}
          <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-zinc-950/50 to-transparent flex items-end p-6">
            <div className="space-y-2">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Compass className="w-4 h-4 text-[#f7931a]" />
                <span>Strategic Direction</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Target className="w-4 h-4 text-[#f7931a]" />
                <span>Clear Priorities</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Map className="w-4 h-4 text-[#f7931a]" />
                <span>Actionable Roadmap</span>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );

  return (
    <div className="bg-zinc-950 text-white">
      <ServiceHero
        headline={t.hero.headline}
        subline={t.hero.subline}
        primaryCTAText={t.hero.primaryCTA}
        secondaryCTAText={t.hero.secondaryCTA}
        onPrimaryCTA={onContact}
        onSecondaryCTA={() => document.getElementById('examples')?.scrollIntoView({ behavior: 'smooth' })}
        visual={<ConsultingVisual />}
      />

      <QuickCheckButton
        language={language}
        onNavigate={onNavigateToFinder || (() => {})}
      />

      <OutcomesSection
        title={t.outcomes.title}
        description={t.outcomes.description}
        outcomes={t.outcomes.items}
      />

      <ProcessSection
        title={t.process.title}
        subtitle={t.process.subtitle}
        steps={t.process.steps}
      />

      <ExamplesSection
        id="examples"
        title={t.examples.title}
        subtitle={t.examples.subtitle}
        examples={t.examples.items}
      />

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
        primaryCTA={{ text: t.cta.primaryButton, onClick: onContact }}
        secondaryCTA={{ text: t.cta.secondaryButton, onClick: onContact }}
      />

      <StickyCTA
        text={t.stickyCTA.text}
        buttonText={t.stickyCTA.button}
        onCTA={onContact}
      />
    </div>
  );
}