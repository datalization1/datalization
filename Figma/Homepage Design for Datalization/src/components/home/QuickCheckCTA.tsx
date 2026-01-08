import { motion } from 'motion/react';
import { Sparkles } from 'lucide-react';

interface QuickCheckCTAProps {
  language: 'de' | 'en';
  onNavigate: () => void;
}

const translations = {
  de: {
    title: 'Welche Lösung passt zu mir?',
    subtitle: 'Machen Sie unseren 3-Fragen-Check und finden Sie es heraus',
    button: 'Zum Quick-Check',
  },
  en: {
    title: 'Which solution is right for me?',
    subtitle: 'Take our 3-question check and find out',
    button: 'Start Quick-Check',
  },
};

export function QuickCheckCTA({ language, onNavigate }: QuickCheckCTAProps) {
  const t = translations[language];

  return (
    <section className="py-20 bg-zinc-950 relative overflow-hidden">
      {/* Decorative Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#f7931a]/5 rounded-full blur-3xl pointer-events-none"></div>
      
      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto text-center"
        >
          {/* Icon */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="inline-flex items-center justify-center w-20 h-20 bg-[#f7931a]/10 rounded-full mb-8"
          >
            <Sparkles className="w-10 h-10 text-[#f7931a]" />
          </motion.div>

          {/* Title */}
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="text-4xl md:text-5xl mb-6 font-medium"
          >
            {t.title}
          </motion.h2>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="text-zinc-400 mb-10 text-lg md:text-xl max-w-2xl mx-auto"
          >
            {t.subtitle}
          </motion.p>

          {/* CTA Button */}
          <motion.button
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.5, duration: 0.5 }}
            onClick={onNavigate}
            className="group inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/90 text-zinc-950 rounded-full hover:shadow-2xl hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium text-lg"
          >
            {t.button}
            <Sparkles className="w-5 h-5 group-hover:rotate-12 transition-transform duration-300" />
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
}