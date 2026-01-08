import { motion } from 'motion/react';
import { useState } from 'react';
import { Check, ArrowRight } from 'lucide-react';

interface QuickCheckProps {
  title: string;
  questions: string[];
  resultText: string;
  ctaText: string;
  onCTA: () => void;
}

export function QuickCheck({ title, questions, resultText, ctaText, onCTA }: QuickCheckProps) {
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [showResult, setShowResult] = useState(false);

  const toggleQuestion = (index: number) => {
    const newSelected = new Set(selected);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelected(newSelected);
    setShowResult(newSelected.size > 0);
  };

  return (
    <section className="py-16 bg-zinc-900/30">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl mx-auto"
        >
          <h2 className="text-3xl md:text-4xl mb-3 text-center">{title}</h2>
          <p className="text-zinc-400 text-center mb-8">
            Wählen Sie, was auf Sie zutrifft:
          </p>

          <div className="space-y-3 mb-8">
            {questions.map((question, index) => (
              <button
                key={index}
                onClick={() => toggleQuestion(index)}
                className={`w-full text-left p-5 rounded-xl border transition-all duration-300 ${
                  selected.has(index)
                    ? 'border-[#f7931a] bg-[#f7931a]/10'
                    : 'border-zinc-800 bg-zinc-900/50 hover:border-zinc-700'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                      selected.has(index)
                        ? 'border-[#f7931a] bg-[#f7931a]'
                        : 'border-zinc-600'
                    }`}
                  >
                    {selected.has(index) && <Check className="w-4 h-4 text-zinc-950" />}
                  </div>
                  <span className={selected.has(index) ? 'text-white' : 'text-zinc-300'}>
                    {question}
                  </span>
                </div>
              </button>
            ))}
          </div>

          {showResult && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-6 bg-gradient-to-br from-[#f7931a]/10 to-transparent border border-[#f7931a]/30 rounded-xl"
            >
              <p className="text-lg mb-4">✓ {resultText}</p>
              <button
                onClick={onCTA}
                className="group inline-flex items-center gap-2 px-6 py-3 bg-[#f7931a] text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 font-medium"
              >
                {ctaText}
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </motion.div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
