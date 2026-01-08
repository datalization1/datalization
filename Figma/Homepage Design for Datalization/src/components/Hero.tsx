import { motion } from 'motion/react';
import { ArrowDown } from 'lucide-react';

interface HeroProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    tagline: 'Einfachheit trifft Innovation',
    subtitle: 'Daten vereinfachen. Zukunft gestalten.',
    description: 'Wir transformieren komplexe Daten in klare Lösungen und digitalisieren Ihre Prozesse mit Weitblick und Loyalität.',
    cta: 'Entdecken Sie mehr',
  },
  en: {
    tagline: 'Simplicity meets Innovation',
    subtitle: 'Simplify Data. Shape the Future.',
    description: 'We transform complex data into clear solutions and digitalize your processes with vision and loyalty.',
    cta: 'Discover More',
  },
};

export function Hero({ language }: HeroProps) {
  const t = translations[language];

  const scrollToServices = () => {
    const element = document.getElementById('services');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-zinc-950">
      {/* Background Effects */}
      <div className="absolute inset-0">
        {/* Gradient orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[#f7931a]/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-[#f7931a]/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 z-10 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.2 }}
            className="inline-block mb-6 px-6 py-2 border border-[#f7931a]/30 rounded-full backdrop-blur-sm bg-[#f7931a]/5"
          >
            <span className="text-[#f7931a]">DATALIZATION</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-5xl md:text-7xl mb-6 bg-gradient-to-r from-zinc-100 via-[#f7931a] to-zinc-100 bg-clip-text text-transparent"
          >
            {t.tagline}
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="text-xl md:text-2xl text-[#f7931a] mb-4"
          >
            {t.subtitle}
          </motion.p>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.7 }}
            className="text-zinc-400 max-w-2xl mx-auto mb-12"
          >
            {t.description}
          </motion.p>

          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.9 }}
            onClick={scrollToServices}
            className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105"
          >
            {t.cta}
            <ArrowDown className="w-4 h-4 group-hover:translate-y-1 transition-transform" />
          </motion.button>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.5 }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-6 h-10 border-2 border-[#f7931a]/50 rounded-full flex items-start justify-center p-2"
        >
          <motion.div className="w-1.5 h-1.5 bg-[#f7931a] rounded-full" />
        </motion.div>
      </motion.div>
    </section>
  );
}