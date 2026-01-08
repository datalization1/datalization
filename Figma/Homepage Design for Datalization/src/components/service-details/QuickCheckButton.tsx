import { motion } from 'motion/react';
import { Sparkles } from 'lucide-react';

interface QuickCheckButtonProps {
  language: 'de' | 'en';
  onNavigate: () => void;
}

const translations = {
  de: {
    title: 'Passt diese Lösung zu mir?',
    subtitle: 'Machen Sie unseren 3-Fragen-Check und finden Sie es heraus',
    button: 'Zum Quick-Check',
  },
  en: {
    title: 'Is this solution right for me?',
    subtitle: 'Take our 3-question check and find out',
    button: 'Start Quick-Check',
  },
};

export function QuickCheckButton({ language, onNavigate }: QuickCheckButtonProps) {
  const t = translations[language];

  return (
    <section className="py-16 bg-zinc-900/30">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-2xl mx-auto text-center"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-[#f7931a]/10 rounded-full mb-6">
            <Sparkles className="w-8 h-8 text-[#f7931a]" />
          </div>
          <h2 className="text-3xl md:text-4xl mb-4">{t.title}</h2>
          <p className="text-zinc-400 mb-8 text-lg">{t.subtitle}</p>
          <button
            onClick={onNavigate}
            className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/90 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium text-lg"
          >
            {t.button}
            <Sparkles className="w-5 h-5" />
          </button>
        </motion.div>
      </div>
    </section>
  );
}
