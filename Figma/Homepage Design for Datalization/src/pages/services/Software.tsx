import { ServiceHero } from '../../components/service-details/ServiceHero';
import { QuickCheckButton } from '../../components/service-details/QuickCheckButton';
import { OutcomesSection } from '../../components/service-details/OutcomesSection';
import { ProcessSection } from '../../components/service-details/ProcessSection';
import { ExamplesSection } from '../../components/service-details/ExamplesSection';
import { DeliverablesSection } from '../../components/service-details/DeliverablesSection';
import { FAQSection } from '../../components/service-details/FAQSection';
import { CTASection } from '../../components/service-details/CTASection';
import { StickyCTA } from '../../components/service-details/StickyCTA';
import { Code, Zap, Shield, Smartphone, Cloud, Lock, CheckCircle, Wrench, Target, BarChart3, TrendingUp, Users } from 'lucide-react';
import { motion } from 'framer-motion';
import { ImageWithFallback } from '../../components/figma/ImageWithFallback';

interface SoftwareProps {
  language: 'de' | 'en';
  onContact: () => void;
  onNavigateToFinder?: () => void;
}

const content = {
  de: {
    hero: {
      headline: 'Software, die mitdenkt',
      subline: 'Wir entwickeln individuelle Lösungen, die genau zu Ihren Prozessen passen – ohne Umwege, ohne Ballast.',
      primaryCTA: 'Kurz-Check buchen',
      secondaryCTA: 'Beispiel ansehen',
    },
    quickCheck: {
      title: 'Passt das zu Ihnen?',
      questions: [
        'Unsere Tools passen nicht zu unseren Abläufen',
        'Wir verbringen zu viel Zeit mit manueller Arbeit',
        'Standard-Software bietet nicht, was wir brauchen',
        'Wir haben Ideen, aber keine Umsetzung',
        'Verschiedene Systeme sprechen nicht miteinander',
        'Wir möchten Prozesse automatisieren',
      ],
      result: 'Individuelle Softwareentwicklung könnte genau das Richtige für Sie sein.',
      cta: 'Kostenlosen 20-Minuten Check buchen',
    },
    outcomes: {
      title: 'Was Sie am Ende haben',
      description: 'Software, die Ihre Arbeit vereinfacht – nicht komplizierter macht.',
      items: [
        'Automatisierte Workflows – weniger Klicks, mehr Ergebnis',
        'Schnittstellen zwischen bestehenden Systemen',
        'Individuelle Web-Apps oder Mobile-Lösungen nach Ihren Wünschen',
        'Wartbare und erweiterbare Software-Architektur',
        'Klare Dokumentation und Einarbeitung Ihres Teams',
        'Skalierbare Lösungen, die mit Ihrem Wachstum mitwachsen',
      ],
    },
    process: {
      title: 'Wie wir vorgehen',
      subtitle: 'Strukturiert, transparent und auf Ihre Bedürfnisse abgestimmt.',
      steps: [
        {
          icon: Target,
          title: 'Verstehen',
          description: 'Wir analysieren Ihre Prozesse und identifizieren Automatisierungspotenziale',
        },
        {
          icon: Code,
          title: 'Konzipieren',
          description: 'Gemeinsam entwickeln wir ein klares Konzept mit Prototypen und Meilensteinen',
        },
        {
          icon: Wrench,
          title: 'Entwickeln',
          description: 'Agile Entwicklung mit regelmäßigen Feedback-Schleifen und Tests',
        },
        {
          icon: CheckCircle,
          title: 'Übergeben',
          description: 'Deployment, Schulung Ihres Teams und laufende Unterstützung',
        },
      ],
    },
    examples: {
      title: 'Typische Projekte',
      subtitle: 'Individuelle Lösungen für verschiedene Branchen',
      items: [
        {
          icon: Zap,
          industry: 'Workflow-Automatisierung',
          scenario: 'Automatische Verarbeitung von Anfragen, Rechnungen oder Bestellungen',
        },
        {
          icon: Cloud,
          industry: 'Cloud-Anwendungen',
          scenario: 'Skalierbare Web-Apps mit modernen Technologien (React, Node.js, Python)',
        },
        {
          icon: Smartphone,
          industry: 'Mobile Apps',
          scenario: 'Native oder Cross-Platform Apps für iOS und Android',
        },
      ],
    },
    deliverables: {
      title: 'Was Sie konkret erhalten',
      subtitle: 'Vollständige Lösungen, die Sie sofort nutzen können',
      items: [
        { icon: Code, title: 'Sauberer, dokumentierter Quellcode', description: 'Gut strukturiert und wartbar' },
        { icon: CheckCircle, title: 'Getestete und deployment-bereite Software', description: 'Produktionsreif und sicher' },
        { icon: Shield, title: 'Sicherheits- und Performance-Optimierung', description: 'Best Practices inklusive' },
        { icon: Wrench, title: 'Technische Dokumentation und Admin-Zugang', description: 'Für vollständige Kontrolle' },
        { icon: Cloud, title: 'Deployment-Setup (Cloud oder On-Premise)', description: 'Nach Ihren Anforderungen' },
        { icon: Zap, title: 'Schulung und Support für Ihr Team', description: 'Damit Sie durchstarten können' },
      ],
    },
    faq: {
      title: 'Häufige Fragen',
      subtitle: 'Antworten auf die wichtigsten Fragen',
      items: [
        {
          question: 'Wie lange dauert ein Software-Projekt?',
          answer: 'Das hängt vom Umfang ab. Kleine Tools können in 4–6 Wochen fertig sein, komplexe Anwendungen benötigen 3–6 Monate. Wir arbeiten agil, sodass Sie früh erste Ergebnisse sehen.',
        },
        {
          question: 'Was kostet individuelle Software?',
          answer: 'Die Kosten variieren je nach Komplexität. Einfache Automatisierungen starten bei CHF 5\'000–10\'000, umfangreichere Projekte bei CHF 20\'000+. Wir erstellen ein transparentes Angebot nach dem Erstgespräch.',
        },
        {
          question: 'Welche Technologien nutzen Sie?',
          answer: 'Wir arbeiten mit modernen, bewährten Technologien: React, TypeScript, Python, Node.js, PostgreSQL. Die Wahl hängt von Ihren Anforderungen ab – wir beraten Sie gerne.',
        },
        {
          question: 'Kann ich die Software später selbst erweitern?',
          answer: 'Ja, wir entwickeln mit sauberem Code und guter Dokumentation. Sie erhalten vollen Zugriff und können die Software intern oder mit anderen Entwicklern weiterentwickeln.',
        },
        {
          question: 'Bieten Sie auch Wartung und Support an?',
          answer: 'Ja, wir bieten flexible Wartungsverträge an. Von punktueller Unterstützung bis zu laufendem Support – je nach Ihrem Bedarf.',
        },
      ],
    },
    cta: {
      title: 'Bereit für Software, die wirklich passt?',
      description: 'Buchen Sie einen kostenlosen 20-Minuten Check. Wir besprechen Ihre Situation und zeigen auf, wie individuelle Software Ihren Alltag erleichtern kann.',
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
      headline: 'Software that thinks ahead',
      subline: 'We develop custom solutions that fit your processes perfectly – no detours, no bloat.',
      primaryCTA: 'Book Quick Check',
      secondaryCTA: 'See Example',
    },
    quickCheck: {
      title: 'Is this right for you?',
      questions: [
        'Our tools don\'t match our workflows',
        'We spend too much time on manual work',
        'Standard software doesn\'t offer what we need',
        'We have ideas but no implementation',
        'Different systems don\'t communicate',
        'We want to automate processes',
      ],
      result: 'Custom software development could be exactly what you need.',
      cta: 'Book Free 20-Minute Check',
    },
    outcomes: {
      title: 'What you\'ll have in the end',
      description: 'Software that simplifies your work – not complicates it.',
      items: [
        'Automated workflows – fewer clicks, more results',
        'Interfaces between existing systems',
        'Custom web apps or mobile solutions to your specifications',
        'Maintainable and extensible software architecture',
        'Clear documentation and team training',
        'Scalable solutions that grow with your business',
      ],
    },
    process: {
      title: 'Our Approach',
      subtitle: 'Structured, transparent, and tailored to your needs.',
      steps: [
        {
          icon: Target,
          title: 'Understand',
          description: 'We analyze your processes and identify automation opportunities',
        },
        {
          icon: Code,
          title: 'Concept',
          description: 'Together we develop a clear concept with prototypes and milestones',
        },
        {
          icon: Wrench,
          title: 'Develop',
          description: 'Agile development with regular feedback loops and testing',
        },
        {
          icon: CheckCircle,
          title: 'Deploy',
          description: 'Deployment, team training, and ongoing support',
        },
      ],
    },
    examples: {
      title: 'Typical Projects',
      subtitle: 'Custom solutions for various industries',
      items: [
        {
          icon: Zap,
          industry: 'Workflow Automation',
          scenario: 'Automatic processing of requests, invoices, or orders',
        },
        {
          icon: Cloud,
          industry: 'Cloud Applications',
          scenario: 'Scalable web apps with modern technologies (React, Node.js, Python)',
        },
        {
          icon: Smartphone,
          industry: 'Mobile Apps',
          scenario: 'Native or cross-platform apps for iOS and Android',
        },
      ],
    },
    deliverables: {
      title: 'What you\'ll receive',
      subtitle: 'Complete solutions you can use immediately',
      items: [
        { icon: Code, title: 'Clean, documented source code', description: 'Well-structured and maintainable' },
        { icon: CheckCircle, title: 'Tested and deployment-ready software', description: 'Production-ready and secure' },
        { icon: Shield, title: 'Security and performance optimization', description: 'Best practices included' },
        { icon: Wrench, title: 'Technical documentation and admin access', description: 'For full control' },
        { icon: Cloud, title: 'Deployment setup (cloud or on-premise)', description: 'According to your requirements' },
        { icon: Zap, title: 'Training and support for your team', description: 'So you can get started' },
      ],
    },
    faq: {
      title: 'Frequently Asked Questions',
      subtitle: 'Answers to the most important questions',
      items: [
        {
          question: 'How long does a software project take?',
          answer: 'It depends on the scope. Small tools can be ready in 4–6 weeks, complex applications need 3–6 months. We work agile, so you see results early.',
        },
        {
          question: 'What does custom software cost?',
          answer: 'Costs vary by complexity. Simple automations start at CHF 5,000–10,000, larger projects at CHF 20,000+. We create a transparent quote after the initial consultation.',
        },
        {
          question: 'Which technologies do you use?',
          answer: 'We work with modern, proven technologies: React, TypeScript, Python, Node.js, PostgreSQL. The choice depends on your requirements – we\'re happy to advise.',
        },
        {
          question: 'Can I extend the software myself later?',
          answer: 'Yes, we develop with clean code and good documentation. You get full access and can continue development internally or with other developers.',
        },
        {
          question: 'Do you also offer maintenance and support?',
          answer: 'Yes, we offer flexible maintenance contracts. From ad-hoc support to ongoing service – depending on your needs.',
        },
      ],
    },
    cta: {
      title: 'Ready for software that truly fits?',
      description: 'Book a free 20-minute check. We\'ll discuss your situation and show how custom software can simplify your daily work.',
      primaryButton: 'Book Check',
      secondaryButton: 'Or write to us',
    },
    stickyCTA: {
      text: 'Learn more?',
      button: 'Book Check',
    },
  },
};

export function Software({ language, onContact, onNavigateToFinder }: SoftwareProps) {
  const t = content[language];

  // Hero Visual - Code Editor with Image
  const SoftwareVisual = () => (
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
            src="https://images.unsplash.com/photo-1531498860502-7c67cf02f657?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzb2Z0d2FyZSUyMGRldmVsb3BtZW50JTIwY29kaW5nfGVufDF8fHx8MTc2Nzc5NjA3NXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
            alt="Software Development"
            className="w-full h-full object-cover"
          />
          {/* Overlay with code snippets */}
          <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-zinc-950/50 to-transparent flex items-end p-6">
            <div className="space-y-2">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Code className="w-4 h-4 text-[#f7931a]" />
                <span>Clean Code</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Shield className="w-4 h-4 text-[#f7931a]" />
                <span>Secure & Scalable</span>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 }}
                className="flex items-center gap-2 text-sm text-zinc-400"
              >
                <Zap className="w-4 h-4 text-[#f7931a]" />
                <span>Modern Technologies</span>
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
        visual={<SoftwareVisual />}
      />

      <QuickCheckButton
        language={language}
        onNavigate={onNavigateToFinder || (() => {})}
      />

      <OutcomesSection
        title={t.outcomes.title}
        description={t.outcomes.description}
        outcomes={t.outcomes.items}
        backgroundImage="https://images.unsplash.com/photo-1742072594013-c87f855e29ca?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzb2Z0d2FyZSUyMGNvZGUlMjBkZXZlbG9wbWVudCUyMHNjcmVlbnxlbnwxfHx8fDE3Njc5NDYwMDF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
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