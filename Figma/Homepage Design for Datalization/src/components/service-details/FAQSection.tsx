import { motion } from 'motion/react';
import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface FAQ {
  question: string;
  answer: string;
}

interface FAQSectionProps {
  title: string;
  subtitle?: string;
  faqs: FAQ[];
}

export function FAQSection({ title, subtitle, faqs }: FAQSectionProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="py-20 bg-zinc-950">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl mb-4">{title}</h2>
          {subtitle && (
            <p className="text-zinc-400 text-lg max-w-2xl mx-auto">{subtitle}</p>
          )}
        </motion.div>

        <div className="max-w-3xl mx-auto space-y-4">
          {faqs.map((faq, index) => {
            const isOpen = openIndex === index;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
                className="group"
              >
                <button
                  onClick={() => toggleFAQ(index)}
                  className={`w-full text-left p-6 rounded-xl border transition-all duration-300 ${
                    isOpen
                      ? 'border-[#f7931a]/50 bg-[#f7931a]/5'
                      : 'border-zinc-800 bg-zinc-900/50 hover:border-zinc-700'
                  }`}
                >
                  <div className="flex items-center justify-between gap-4">
                    <h3 className={`text-lg font-medium ${isOpen ? 'text-[#f7931a]' : 'text-white'}`}>
                      {faq.question}
                    </h3>
                    <ChevronDown
                      className={`flex-shrink-0 w-5 h-5 transition-transform duration-300 ${
                        isOpen ? 'rotate-180 text-[#f7931a]' : 'text-zinc-400'
                      }`}
                    />
                  </div>

                  {isOpen && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.3 }}
                      className="mt-4 pt-4 border-t border-zinc-800"
                    >
                      <p className="text-zinc-300 leading-relaxed">{faq.answer}</p>
                    </motion.div>
                  )}
                </button>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
