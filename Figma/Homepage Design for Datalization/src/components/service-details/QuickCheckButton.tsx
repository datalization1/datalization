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
    <section className="relative py-20 bg-gradient-to-b from-[#0f0f11] via-[#0c0c0e] to-[#0a0a0b] overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(247,147,26,0.12),transparent_38%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_78%_10%,rgba(247,147,26,0.08),transparent_36%)]" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl mx-auto text-center"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-[#f7931a]/10 border border-[#f7931a]/35 rounded-full mb-6 shadow-[0_14px_36px_rgba(247,147,26,0.28)]">
            <Sparkles className="w-8 h-8 text-[#f7931a]" strokeWidth={2.25} />
          </div>
          <h2 className="text-3xl md:text-4xl font-semibold mb-3">{t.title}</h2>
          <p className="text-zinc-400 mb-9 text-lg">{t.subtitle}</p>
          <button
            onClick={onNavigate}
            className="inline-flex items-center gap-3 px-9 py-4 bg-gradient-to-b from-[#f9a028] to-[#f4830f] text-zinc-950 rounded-full font-semibold text-lg shadow-[0_16px_38px_rgba(247,147,26,0.38)] border border-[#f7931a]/70 hover:shadow-[0_18px_44px_rgba(247,147,26,0.45)] hover:scale-105 transition-transform duration-200"
          >
            {t.button}
            <Sparkles className="w-5 h-5" />
          </button>
        </motion.div>
      </div>
    </section>
  );
}
