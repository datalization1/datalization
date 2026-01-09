import { motion, AnimatePresence } from 'motion/react';
import { useState } from 'react';
import { ChevronRight, ChevronLeft, Sparkles, ArrowRight } from 'lucide-react';
import { Button } from './ui/button';

interface ServiceFinderProps {
  language: 'de' | 'en';
  onServiceClick: (serviceId: string) => void;
  scrollToContact: () => void;
}

const translations = {
  de: {
    title: 'Was passt zu dir?',
    subtitle: 'Drei kurze Fragen – und du weisst, wie wir dir helfen können',
    nextButton: 'Weiter',
    backButton: 'Zurück',
    showResult: 'Ergebnis anzeigen',
    resultTitle: 'Basierend auf deinen Antworten scheint Folgendes gut zu passen:',
    resultSubtitle: 'Im Gespräch schauen wir gemeinsam, was davon wirklich Sinn macht – und was nicht.',
    ctaPrimary: 'Unverbindlich besprechen',
    ctaSecondary: 'Mehr erfahren',
    questions: [
      {
        title: 'Wo stehst du gerade?',
        subtitle: 'Was beschreibt deine aktuelle Situation am besten?',
        type: 'multi' as const,
        options: [
          { id: 'no-overview', label: 'Ich habe Zahlen, aber keinen Überblick', scores: { 'data-analytics': 2, 'consulting': 1 } },
          { id: 'excel', label: 'Ich arbeite viel mit Excel oder Listen', scores: { 'software': 2, 'digitalization': 1 } },
          { id: 'manual', label: 'Viele Dinge laufen noch manuell', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'systems', label: 'Unsere Systeme passen nicht richtig zusammen', scores: { 'software': 2, 'consulting': 1 } },
          { id: 'profit', label: 'Ich weiss nicht genau, wo wir Geld verdienen oder verlieren', scores: { 'data-analytics': 2, 'consulting': 1 } },
        ],
      },
      {
        title: 'Was macht dir im Alltag am meisten Mühe?',
        subtitle: 'Was kostet dich aktuell am meisten Energie?',
        type: 'multi' as const,
        options: [
          { id: 'decisions', label: 'Entscheidungen fühlen sich unsicher an', scores: { 'data-analytics': 2, 'consulting': 1 } },
          { id: 'admin', label: 'Zu viel Zeit geht für Administration drauf', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'reactive', label: 'Ich reagiere mehr, als dass ich planen kann', scores: { 'consulting': 2, 'data-analytics': 1 } },
          { id: 'distributed', label: 'Informationen sind überall verteilt', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'no-time', label: 'Ich habe zu wenig Zeit fürs Kerngeschäft', scores: { 'digitalization': 1, 'consulting': 1, 'software': 1 } },
        ],
      },
      {
        title: 'Was wünschst du dir stattdessen?',
        subtitle: 'Was würde dir den grössten Mehrwert bringen?',
        type: 'multi' as const,
        options: [
          { id: 'overview', label: 'Klarer Überblick auf einen Blick', scores: { 'data-analytics': 2, 'software': 1 } },
          { id: 'automation', label: 'Weniger manuelle Arbeit', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'planning', label: 'Bessere Planung & ruhigere Entscheidungen', scores: { 'data-analytics': 2, 'consulting': 1 } },
          { id: 'processes', label: 'Abläufe, die einfach funktionieren', scores: { 'software': 2, 'digitalization': 1 } },
          { id: 'clarity', label: 'Ein klarer Plan, was sich wirklich lohnt', scores: { 'consulting': 2, 'data-analytics': 1 } },
        ],
      },
    ],
    services: {
      'data-analytics': {
        title: 'Datenanalyse & Data Science',
        description: 'Könnte dir helfen, Klarheit zu gewinnen und sicherer zu entscheiden.',
        icon: '📊',
      },
      'digitalization': {
        title: 'Digitalisierung',
        description: 'Hilft dir, manuelle Arbeit zu reduzieren und Abläufe zu vereinfachen.',
        icon: '⚙️',
      },
      'software': {
        title: 'Softwareentwicklung',
        description: 'Kann Prozesse verbinden und deinen Alltag deutlich vereinfachen.',
        icon: '💻',
      },
      'consulting': {
        title: 'Beratung & Strategie',
        description: 'Hilft dir, Prioritäten zu setzen und einen sinnvollen Weg festzulegen.',
        icon: '🧭',
      },
    },
  },
  en: {
    title: 'What fits your needs?',
    subtitle: 'Three quick questions – and you\\\'ll know how we can help',
    nextButton: 'Next',
    backButton: 'Back',
    showResult: 'Show result',
    resultTitle: 'Based on your answers, the following seems to be a good fit:',
    resultSubtitle: 'In a conversation, we\\\'ll look together at what really makes sense – and what doesn\\\'t.',
    ctaPrimary: 'Schedule a call',
    ctaSecondary: 'Learn more',
    questions: [
      {
        title: 'Where are you right now?',
        subtitle: 'What best describes your current situation?',
        type: 'multi' as const,
        options: [
          { id: 'no-overview', label: 'I have data, but no overview', scores: { 'data-analytics': 2, 'consulting': 1 } },
          { id: 'excel', label: 'I work a lot with Excel or lists', scores: { 'software': 2, 'digitalization': 1 } },
          { id: 'manual', label: 'Many things are still done manually', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'systems', label: 'Our systems don\\\'t fit together properly', scores: { 'software': 2, 'consulting': 1 } },
          { id: 'profit', label: 'I don\\\'t know exactly where we make or lose money', scores: { 'data-analytics': 2, 'consulting': 1 } },
        ],
      },
      {
        title: 'What causes you the most trouble in everyday life?',
        subtitle: 'What currently costs you the most energy?',
        type: 'multi' as const,
        options: [
          { id: 'decisions', label: 'Decisions feel uncertain', scores: { 'data-analytics': 2, 'consulting': 1 } },
          { id: 'admin', label: 'Too much time spent on administration', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'reactive', label: 'I react more than I plan', scores: { 'consulting': 2, 'data-analytics': 1 } },
          { id: 'distributed', label: 'Information is everywhere', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'no-time', label: 'I have too little time for core business', scores: { 'digitalization': 1, 'consulting': 1, 'software': 1 } },
        ],
      },
      {
        title: 'What would you like instead?',
        subtitle: 'What would bring you the greatest benefit?',
        type: 'multi' as const,
        options: [
          { id: 'overview', label: 'Clear overview at a glance', scores: { 'data-analytics': 2, 'software': 1 } },
          { id: 'automation', label: 'Less manual work', scores: { 'digitalization': 2, 'software': 1 } },
          { id: 'planning', label: 'Better planning & calmer decisions', scores: { 'data-analytics': 2, 'consulting': 1 } },
          { id: 'processes', label: 'Processes that simply work', scores: { 'software': 2, 'digitalization': 1 } },
          { id: 'clarity', label: 'A clear plan of what really pays off', scores: { 'consulting': 2, 'data-analytics': 1 } },
        ],
      },
    ],
    services: {
      'data-analytics': {
        title: 'Data Analysis & Data Science',
        description: 'Could help you gain clarity and make more confident decisions.',
        icon: '📊',
      },
      'digitalization': {
        title: 'Digitalization',
        description: 'Helps you reduce manual work and simplify processes.',
        icon: '⚙️',
      },
      'software': {
        title: 'Software Development',
        description: 'Can connect processes and significantly simplify your daily work.',
        icon: '💻',
      },
      'consulting': {
        title: 'Consulting & Strategy',
        description: 'Helps you set priorities and define a meaningful path.',
        icon: '🧭',
      },
    },
  },
};

export function ServiceFinder({ language, onServiceClick, scrollToContact }: ServiceFinderProps) {
  const t = translations[language];
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: string[] }>({});
  const [showResult, setShowResult] = useState(false);

  const currentQuestion = t.questions[currentStep];
  const isLastQuestion = currentStep === t.questions.length - 1;

  const handleOptionSelect = (optionId: string) => {
    if (currentQuestion.type === 'single') {
      setAnswers({ ...answers, [currentStep]: [optionId] });
    } else {
      const currentAnswers = answers[currentStep] || [];
      if (currentAnswers.includes(optionId)) {
        // Remove if already selected
        setAnswers({
          ...answers,
          [currentStep]: currentAnswers.filter((id) => id !== optionId),
        });
      } else {
        // Add if not at max selections
        if (!currentQuestion.maxSelections || currentAnswers.length < currentQuestion.maxSelections) {
          setAnswers({
            ...answers,
            [currentStep]: [...currentAnswers, optionId],
          });
        }
      }
    }
  };

  const canProceed = () => {
    const currentAnswers = answers[currentStep];
    return currentAnswers && currentAnswers.length > 0;
  };

  const handleNext = () => {
    if (isLastQuestion) {
      setShowResult(true);
    } else {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (showResult) {
      setShowResult(false);
    } else if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const calculateResults = () => {
    const scores: { [key: string]: number } = {
      'data-analytics': 0,
      'digitalization': 0,
      'software': 0,
      'consulting': 0,
    };

    // Calculate scores based on answers
    Object.entries(answers).forEach(([stepIndex, selectedOptions]) => {
      const question = t.questions[parseInt(stepIndex)];
      selectedOptions.forEach((optionId) => {
        const option = question.options.find((opt) => opt.id === optionId);
        if (option?.scores) {
          Object.entries(option.scores).forEach(([service, points]) => {
            scores[service] += points;
          });
        }
      });
    });

    // Get top 2 services
    const sortedServices = Object.entries(scores)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 2)
      .filter(([, score]) => score > 0);

    return sortedServices.map(([serviceId]) => serviceId);
  };

  const recommendedServices = showResult ? calculateResults() : [];

  if (showResult) {
    return (
      <section id="service-finder" className="py-24 scroll-mt-20">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="bg-zinc-900/50 backdrop-blur-sm border border-[#f7931a]/30 rounded-3xl p-8 md:p-12"
            >
              {/* Header */}
              <div className="text-center mb-10">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-[#f7931a]/10 rounded-full mb-6">
                  <Sparkles className="w-8 h-8 text-[#f7931a]" />
                </div>
                <h3 className="text-3xl mb-4">{t.resultTitle}</h3>
                <p className="text-zinc-400">{t.resultSubtitle}</p>
              </div>

              {/* Recommended Services */}
              <div className="space-y-4 mb-10">
                {recommendedServices.map((serviceId, index) => {
                  const service = t.services[serviceId as keyof typeof t.services];
                  return (
                    <motion.div
                      key={serviceId}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: index * 0.1 }}
                      className="group bg-zinc-800/50 border border-zinc-700 hover:border-[#f7931a]/50 rounded-2xl p-6 transition-all cursor-pointer"
                      onClick={() => onServiceClick(serviceId)}
                    >
                      <div className="flex items-start gap-4">
                        <div className="text-4xl">{service.icon}</div>
                        <div className="flex-1">
                          <h4 className="text-xl mb-2 group-hover:text-[#f7931a] transition-colors">
                            {service.title}
                          </h4>
                          <p className="text-zinc-400 text-sm">{service.description}</p>
                        </div>
                        <ArrowRight className="w-5 h-5 text-zinc-500 group-hover:text-[#f7931a] group-hover:translate-x-1 transition-all" />
                      </div>
                    </motion.div>
                  );
                })}
              </div>

              {/* CTAs */}
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  onClick={scrollToContact}
                  className="flex-1 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105"
                >
                  {t.ctaPrimary}
                </Button>
                <Button
                  onClick={handleBack}
                  variant="outline"
                  className="flex-1 border-zinc-700 hover:border-[#f7931a]/50"
                >
                  {t.backButton}
                </Button>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="service-finder" className="py-24 scroll-mt-20 relative overflow-hidden">
      {/* Background Effect */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#f7931a]/5 to-transparent pointer-events-none" />

      <div className="container mx-auto px-4 relative">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4">{t.title}</h2>
          <p className="text-zinc-400 max-w-2xl mx-auto">{t.subtitle}</p>
        </motion.div>

        <div className="max-w-3xl mx-auto">
          <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-3xl p-8 md:p-12">
            {/* Progress Bar */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-zinc-500">
                  Frage {currentStep + 1} von {t.questions.length}
                </span>
                <span className="text-sm text-zinc-500">
                  {Math.round(((currentStep + 1) / t.questions.length) * 100)}%
                </span>
              </div>
              <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80"
                  initial={{ width: 0 }}
                  animate={{ width: `${((currentStep + 1) / t.questions.length) * 100}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>
            </div>

            {/* Question */}
            <AnimatePresence mode="wait">
              <motion.div
                key={currentStep}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <h3 className="text-2xl md:text-3xl mb-3">{currentQuestion.title}</h3>
                <p className="text-zinc-400 mb-8">{currentQuestion.subtitle}</p>

                {/* Options */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                  {currentQuestion.options.map((option, index) => {
                    const isSelected = answers[currentStep]?.includes(option.id);
                    const isMulti = currentQuestion.type === 'multi';
                    const atMaxSelections = isMulti && currentQuestion.maxSelections && 
                      (answers[currentStep]?.length || 0) >= currentQuestion.maxSelections;
                    const isDisabled = isMulti && atMaxSelections && !isSelected;
                    
                    return (
                      <motion.button
                        key={option.id}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.3, delay: index * 0.05 }}
                        onClick={() => handleOptionSelect(option.id)}
                        disabled={isDisabled}
                        className={`group relative text-left p-6 rounded-2xl border-2 transition-all duration-300 ${
                          isSelected
                            ? 'border-[#f7931a] bg-gradient-to-br from-[#f7931a]/20 to-[#f7931a]/5 shadow-lg shadow-[#f7931a]/20'
                            : isDisabled
                            ? 'border-zinc-800 bg-zinc-900/30 opacity-50 cursor-not-allowed'
                            : 'border-zinc-800 bg-zinc-900/50 hover:border-zinc-700 hover:bg-zinc-800/50 hover:shadow-lg hover:scale-[1.02]'
                        }`}
                      >
                        {/* Selection Indicator */}
                        <div className="absolute top-4 right-4">
                          <div
                            className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                              isSelected 
                                ? 'border-[#f7931a] bg-[#f7931a]' 
                                : 'border-zinc-600 group-hover:border-zinc-500'
                            }`}
                          >
                            {isSelected && (
                              <motion.svg
                                initial={{ scale: 0, rotate: -180 }}
                                animate={{ scale: 1, rotate: 0 }}
                                className="w-4 h-4 text-zinc-950"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth={3}
                              >
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                              </motion.svg>
                            )}
                          </div>
                        </div>

                        {/* Card Content */}
                        <div className="pr-8">
                          <p className={`text-base leading-relaxed transition-colors ${
                            isSelected ? 'text-white font-medium' : 'text-zinc-300 group-hover:text-white'
                          }`}>
                            {option.label}
                          </p>
                        </div>

                        {/* Hover Effect Border Glow */}
                        {!isDisabled && !isSelected && (
                          <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-[#f7931a]/0 to-[#f7931a]/0 group-hover:from-[#f7931a]/5 group-hover:to-transparent transition-all duration-300 pointer-events-none" />
                        )}
                      </motion.button>
                    );
                  })}
                </div>
              </motion.div>
            </AnimatePresence>

            {/* Navigation Buttons */}
            <div className="flex gap-4">
              {currentStep > 0 && (
                <Button onClick={handleBack} variant="outline" className="gap-2 border-zinc-700">
                  <ChevronLeft className="w-4 h-4" />
                  {t.backButton}
                </Button>
              )}
              <Button
                onClick={handleNext}
                disabled={!canProceed()}
                className="flex-1 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed gap-2"
              >
                {isLastQuestion ? t.showResult : t.nextButton}
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}