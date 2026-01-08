import { motion } from 'motion/react';
import { Lightbulb, Code, Rocket } from 'lucide-react';

interface ApproachProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Unser Ansatz',
    subtitle: 'Von der Idee zur Lösung – in drei Schritten',
    steps: [
      {
        icon: Lightbulb,
        title: 'Verstehen',
        description: 'Wir analysieren Ihre Herausforderungen und verstehen Ihre Bedürfnisse im Detail.',
        details: 'Gemeinsame Workshops, Datenanalyse und Prozess-Mapping schaffen die Grundlage für maßgeschneiderte Lösungen.',
      },
      {
        icon: Code,
        title: 'Entwickeln',
        description: 'Mit agilen Methoden entwickeln wir einfache, skalierbare und zukunftssichere Lösungen.',
        details: 'Moderne Technologien, klare Architektur und iterative Entwicklung garantieren höchste Qualität.',
      },
      {
        icon: Rocket,
        title: 'Wachsen',
        description: 'Wir begleiten Sie auch nach dem Launch – für nachhaltigen Erfolg und kontinuierliche Optimierung.',
        details: 'Support, Training und fortlaufende Weiterentwicklung sichern Ihre digitale Zukunft.',
      },
    ],
  },
  en: {
    title: 'Our Approach',
    subtitle: 'From idea to solution – in three steps',
    steps: [
      {
        icon: Lightbulb,
        title: 'Understand',
        description: 'We analyze your challenges and understand your needs in detail.',
        details: 'Joint workshops, data analysis and process mapping create the foundation for tailored solutions.',
      },
      {
        icon: Code,
        title: 'Develop',
        description: 'Using agile methods, we develop simple, scalable and future-proof solutions.',
        details: 'Modern technologies, clear architecture and iterative development guarantee the highest quality.',
      },
      {
        icon: Rocket,
        title: 'Grow',
        description: 'We accompany you even after launch – for sustainable success and continuous optimization.',
        details: 'Support, training and ongoing development secure your digital future.',
      },
    ],
  },
};

export function Approach({ language }: ApproachProps) {
  const t = translations[language];

  return (
    <section className="py-24 bg-zinc-950 relative overflow-hidden">
      {/* Background gradient effect */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#f7931a]/5 to-transparent pointer-events-none" />
      
      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4">{t.title}</h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            {t.subtitle}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {t.steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="relative group"
              >
                {/* Connection Line - visible only on desktop */}
                {index < t.steps.length - 1 && (
                  <div className="hidden md:block absolute top-12 left-[calc(50%+2rem)] w-[calc(100%-4rem)] h-0.5 bg-gradient-to-r from-[#f7931a]/30 to-transparent z-0" />
                )}
                
                {/* Glassmorphism Card */}
                <div className="relative z-10 bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-8 hover:border-[#f7931a]/50 transition-all duration-300 hover:shadow-lg hover:shadow-[#f7931a]/10">
                  {/* Hover Gradient Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-br from-[#f7931a]/0 to-[#f7931a]/0 group-hover:from-[#f7931a]/5 group-hover:to-transparent rounded-2xl transition-all duration-300" />
                  
                  <div className="relative z-10">
                    {/* Step Number */}
                    <div className="absolute -top-4 -right-4 w-12 h-12 bg-gradient-to-br from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full flex items-center justify-center text-xl font-bold shadow-lg shadow-[#f7931a]/30">
                      {index + 1}
                    </div>

                    {/* Icon */}
                    <div className="w-16 h-16 bg-[#f7931a]/10 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-[#f7931a]/20 transition-colors duration-300 group-hover:scale-110 transform">
                      <Icon className="w-8 h-8 text-[#f7931a]" />
                    </div>
                    
                    <h3 className="text-2xl mb-3 group-hover:text-[#f7931a] transition-colors duration-300">{step.title}</h3>
                    <p className="text-zinc-400 mb-4">{step.description}</p>
                    <p className="text-sm text-zinc-500 group-hover:text-zinc-400 transition-colors duration-300">{step.details}</p>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
