import { ServiceHero } from '../../components/service-details/ServiceHero';
import { QuickCheckButton } from '../../components/service-details/QuickCheckButton';
import { OutcomesSection } from '../../components/service-details/OutcomesSection';
import { ProcessSection } from '../../components/service-details/ProcessSection';
import { ExamplesSection } from '../../components/service-details/ExamplesSection';
import { DeliverablesSection } from '../../components/service-details/DeliverablesSection';
import { FAQSection } from '../../components/service-details/FAQSection';
import { CTASection } from '../../components/service-details/CTASection';
import { StickyCTA } from '../../components/service-details/StickyCTA';
import { Search, Target, Settings, Users, FileText, Workflow, FolderOpen, CheckCircle, Zap, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { ImageWithFallback } from '../../components/figma/ImageWithFallback';

interface DigitalizationProps {
  language: 'de' | 'en';
  onContact: () => void;
  onNavigateToFinder?: () => void;
}

const content = {
  de: {
    hero: {
      headline: 'Weniger Papier, mehr Effizienz',
      subline: 'Wir helfen Ihnen, Abläufe zu vereinfachen und Zeit zu sparen – ohne Chaos, ohne Umstellung auf gut Glück.',
      primaryCTA: 'Kurz-Check buchen',
      secondaryCTA: 'Beispiel ansehen',
    },
    quickCheck: {
      title: 'Passt das zu Ihnen?',
      questions: [
        'Wir arbeiten noch viel mit Papier oder PDFs',
        'Dokumente sind schwer zu finden',
        'Genehmigungsprozesse dauern zu lange',
        'Informationen gehen verloren oder sind nicht aktuell',
        'Wir verbringen zu viel Zeit mit Ablage',
        'Teams arbeiten nicht effizient zusammen',
      ],
      result: 'Digitalisierung könnte genau das Richtige für Sie sein.',
      cta: 'Kostenlosen 20-Minuten Check buchen',
    },
    outcomes: {
      title: 'Was Sie am Ende haben',
      description: 'Digitale Prozesse, die Ihren Alltag erleichtern – nicht verkomplizieren.',
      items: [
        'Zentrale, durchsuchbare Dokumentenablage',
        'Automatisierte Workflows (Freigaben, Rechnungen, Bestellungen)',
        'Weniger Zeitverlust durch manuelle Suche und Weitergabe',
        'Klare Verantwortlichkeiten und Transparenz über Fortschritte',
        'Reduzierte Fehlerquote durch standardisierte Prozesse',
        'Mobiler Zugriff auf wichtige Informationen',
      ],
    },
    process: {
      title: 'Wie wir vorgehen',
      subtitle: 'Schritt für Schritt – ohne Ihr Tagesgeschäft zu stören.',
      steps: [
        {
          icon: Search,
          title: 'Ist-Analyse',
          description: 'Wir schauen uns Ihre aktuellen Abläufe an und identifizieren Engpässe',
        },
        {
          icon: Target,
          title: 'Priorisierung',
          description: 'Gemeinsam entscheiden wir, wo Digitalisierung den größten Nutzen bringt',
        },
        {
          icon: Settings,
          title: 'Umsetzung',
          description: 'Wir implementieren Lösungen Schritt für Schritt – mit Ihrem Team',
        },
        {
          icon: Users,
          title: 'Begleitung',
          description: 'Training, Anpassungen und laufende Unterstützung im Alltag',
        },
      ],
    },
    examples: {
      title: 'Typische Projekte',
      subtitle: 'Digitalisierung in verschiedenen Bereichen',
      items: [
        {
          icon: FileText,
          industry: 'Dokumentenmanagement',
          scenario: 'Digitale Ablage mit Versionierung, Suche und Zugriffsrechten',
        },
        {
          icon: Workflow,
          industry: 'Workflow-Automatisierung',
          scenario: 'Freigabeprozesse, Rechnungsläufe oder Bestellwesen automatisieren',
        },
        {
          icon: Users,
          industry: 'Kollaborationsplattformen',
          scenario: 'Gemeinsame Arbeitsbereiche für Teams (SharePoint, Notion, Custom)',
        },
      ],
    },
    deliverables: {
      title: 'Was Sie konkret erhalten',
      subtitle: 'Vollständige Lösungen für digitale Prozesse',
      items: [
        { icon: FolderOpen, title: 'Strukturiertes Dokumentenmanagement-System', description: 'Zentral und durchsuchbar' },
        { icon: Workflow, title: 'Definierte und automatisierte Workflows', description: 'Für schnellere Abläufe' },
        { icon: CheckCircle, title: 'Schulungsunterlagen und Einführung für Ihr Team', description: 'Damit alle mitkommen' },
        { icon: Zap, title: 'Integration in bestehende Systeme (ERP, CRM, etc.)', description: 'Nahtlose Verbindung' },
        { icon: Users, title: 'Benutzer- und Rechteverwaltung', description: 'Sichere Zugriffssteuerung' },
        { icon: ArrowRight, title: 'Begleitung während der Umstellung', description: 'Wir sind für Sie da' },
      ],
    },
    faq: {
      title: 'Häufige Fragen',
      subtitle: 'Antworten auf die wichtigsten Fragen',
      items: [
        {
          question: 'Wie lange dauert eine Digitalisierung?',
          answer: 'Das hängt vom Umfang ab. Einzelne Prozesse können in 4–6 Wochen digitalisiert werden. Größere Transformationen erstrecken sich über mehrere Monate – wir gehen schrittweise vor.',
        },
        {
          question: 'Was kostet eine Digitalisierung?',
          answer: 'Das variiert je nach Prozess und Lösung. Einfache Workflows starten bei CHF 3\'000–5\'000, umfangreichere Projekte bei CHF 15\'000+. Wir erstellen ein transparentes Angebot nach dem Erstgespräch.',
        },
        {
          question: 'Können wir unsere bestehenden Systeme weiternutzen?',
          answer: 'In der Regel ja. Wir prüfen, ob bestehende Tools erweitert oder integriert werden können, bevor wir neue Systeme vorschlagen.',
        },
        {
          question: 'Wie geht mein Team mit der Umstellung um?',
          answer: 'Wir begleiten die Einführung aktiv und schulen Ihr Team. Change Management und klare Kommunikation sind Teil unseres Ansatzes.',
        },
        {
          question: 'Sind digitale Prozesse sicher?',
          answer: 'Ja, wir achten auf Datenschutz, Zugriffsrechte und Backup-Strategien. Alle Lösungen entsprechen den gängigen Sicherheitsstandards.',
        },
      ],
    },
    cta: {
      title: 'Bereit für digitale Prozesse?',
      description: 'Buchen Sie einen kostenlosen 20-Minuten Check. Wir besprechen Ihre Situation und zeigen auf, wo Digitalisierung Ihnen Zeit und Nerven spart.',
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
      headline: 'Less paper, more efficiency',
      subline: 'We help you simplify workflows and save time – without chaos, without random change.',
      primaryCTA: 'Book Quick Check',
      secondaryCTA: 'See Example',
    },
    quickCheck: {
      title: 'Is this right for you?',
      questions: [
        'We still work a lot with paper or PDFs',
        'Documents are hard to find',
        'Approval processes take too long',
        'Information gets lost or isn\'t current',
        'We spend too much time filing',
        'Teams don\'t collaborate efficiently',
      ],
      result: 'Digitalization could be exactly what you need.',
      cta: 'Book Free 20-Minute Check',
    },
    outcomes: {
      title: 'What you\'ll have in the end',
      description: 'Digital processes that simplify your daily work – not complicate it.',
      items: [
        'Central, searchable document repository',
        'Automated workflows (approvals, invoices, orders)',
        'Less time lost searching and forwarding',
        'Clear responsibilities and progress transparency',
        'Reduced error rate through standardized processes',
        'Mobile access to important information',
      ],
    },
    process: {
      title: 'Our Approach',
      subtitle: 'Step by step – without disrupting your daily business.',
      steps: [
        {
          icon: Search,
          title: 'Current State Analysis',
          description: 'We examine your current workflows and identify bottlenecks',
        },
        {
          icon: Target,
          title: 'Prioritization',
          description: 'Together we decide where digitalization brings the greatest benefit',
        },
        {
          icon: Settings,
          title: 'Implementation',
          description: 'We implement solutions step by step – with your team',
        },
        {
          icon: Users,
          title: 'Support',
          description: 'Training, adjustments, and ongoing support in daily operations',
        },
      ],
    },
    examples: {
      title: 'Typical Projects',
      subtitle: 'Digitalization in various areas',
      items: [
        {
          icon: FileText,
          industry: 'Document Management',
          scenario: 'Digital filing with versioning, search, and access rights',
        },
        {
          icon: Workflow,
          industry: 'Workflow Automation',
          scenario: 'Automate approval processes, invoice runs, or ordering',
        },
        {
          icon: Users,
          industry: 'Collaboration Platforms',
          scenario: 'Shared workspaces for teams (SharePoint, Notion, Custom)',
        },
      ],
    },
    deliverables: {
      title: 'What you\'ll receive',
      subtitle: 'Complete solutions for digital processes',
      items: [
        { icon: FolderOpen, title: 'Structured document management system', description: 'Central and searchable' },
        { icon: Workflow, title: 'Defined and automated workflows', description: 'For faster processes' },
        { icon: CheckCircle, title: 'Training materials and introduction for your team', description: 'So everyone can follow' },
        { icon: Zap, title: 'Integration with existing systems (ERP, CRM, etc.)', description: 'Seamless connection' },
        { icon: Users, title: 'User and permission management', description: 'Secure access control' },
        { icon: ArrowRight, title: 'Support during the transition', description: 'We\'re here for you' },
      ],
    },
    faq: {
      title: 'Frequently Asked Questions',
      subtitle: 'Answers to the most important questions',
      items: [
        {
          question: 'How long does digitalization take?',
          answer: 'It depends on the scope. Individual processes can be digitalized in 4–6 weeks. Larger transformations span several months – we proceed step by step.',
        },
        {
          question: 'What does digitalization cost?',
          answer: 'It varies by process and solution. Simple workflows start at CHF 3,000–5,000, larger projects at CHF 15,000+. We create a transparent quote after the initial consultation.',
        },
        {
          question: 'Can we continue using our existing systems?',
          answer: 'Usually yes. We check if existing tools can be extended or integrated before suggesting new systems.',
        },
        {
          question: 'How will my team handle the transition?',
          answer: 'We actively support the implementation and train your team. Change management and clear communication are part of our approach.',
        },
        {
          question: 'Are digital processes secure?',
          answer: 'Yes, we focus on data protection, access rights, and backup strategies. All solutions comply with common security standards.',
        },
      ],
    },
    cta: {
      title: 'Ready for digital processes?',
      description: 'Book a free 20-minute check. We\'ll discuss your situation and show where digitalization saves you time and nerves.',
      primaryButton: 'Book Check',
      secondaryButton: 'Or write to us',
    },
    stickyCTA: {
      text: 'Learn more?',
      button: 'Book Check',
    },
  },
};

export function Digitalization({ language, onContact, onNavigateToFinder }: DigitalizationProps) {
  const t = content[language];

  // Hero Visual - Digital Transformation
  const DigitalVisual = () => (
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
            src="https://images.unsplash.com/photo-1726607424623-6d9fee974241?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwdHJhbnNmb3JtYXRpb24lMjBidXNpbmVzc3xlbnwxfHx8fDE3Njc4ODgwMjV8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
            alt="Digital Transformation"
            className="w-full h-full object-cover"
          />
          {/* Overlay with workflow icons */}
          <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-zinc-950/50 to-transparent flex items-end p-6">
            <div className="space-y-2">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <FileText className="w-4 h-4 text-[#f7931a]" />
                <span>Paperless</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Workflow className="w-4 h-4 text-[#f7931a]" />
                <span>Automated Workflows</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Zap className="w-4 h-4 text-[#f7931a]" />
                <span>Efficient Processes</span>
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
        visual={<DigitalVisual />}
      />

      <QuickCheckButton
        language={language}
        onNavigate={onNavigateToFinder || (() => {})}
      />

      <OutcomesSection
        title={t.outcomes.title}
        description={t.outcomes.description}
        outcomes={t.outcomes.items}
        backgroundImage="https://images.unsplash.com/photo-1759752393975-7ca7b302fcc6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwd29ya2Zsb3clMjBhdXRvbWF0aW9ufGVufDF8fHx8MTc2NzkwMTY0M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
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