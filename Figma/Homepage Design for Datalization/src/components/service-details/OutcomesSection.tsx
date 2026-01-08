import { motion } from 'motion/react';
import { Check } from 'lucide-react';

interface OutcomesSectionProps {
  title: string;
  description?: string;
  outcomes: string[];
  visual?: React.ReactNode;
}

export function OutcomesSection({ title, description, outcomes, visual }: OutcomesSectionProps) {
  return (
    <section className="py-20 bg-zinc-950">
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 items-center max-w-7xl mx-auto">
          {/* Outcomes List */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl mb-4">{title}</h2>
            {description && (
              <p className="text-zinc-400 text-lg mb-8">{description}</p>
            )}

            <div className="space-y-4">
              {outcomes.map((outcome, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="flex items-start gap-3 group"
                >
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-[#f7931a]/20 flex items-center justify-center group-hover:bg-[#f7931a]/30 transition-colors">
                    <Check className="w-4 h-4 text-[#f7931a]" />
                  </div>
                  <p className="text-zinc-300 group-hover:text-white transition-colors">
                    {outcome}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Visual */}
          {visual && (
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              {visual}
            </motion.div>
          )}
        </div>
      </div>
    </section>
  );
}
