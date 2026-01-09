import { motion } from 'motion/react';
import { Check } from 'lucide-react';

interface OutcomesSectionProps {
  title: string;
  description?: string;
  outcomes: string[];
  visual?: React.ReactNode;
  backgroundImage?: string;
}

export function OutcomesSection({ title, description, outcomes, visual, backgroundImage }: OutcomesSectionProps) {
  return (
    <section className="py-24 bg-zinc-950 relative overflow-hidden">
      {/* Background Image with Overlay */}
      {backgroundImage && (
        <div className="absolute inset-0">
          <div 
            className="absolute inset-0 bg-cover bg-center scale-105 blur-sm opacity-70"
            style={{ backgroundImage: `url(${backgroundImage})` }}
          />
          <div className="absolute inset-0 bg-gradient-to-b from-[#0b0b0d]/92 via-[#0b0b0d]/88 to-[#0b0b0d]/95" />
        </div>
      )}
      
      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-start max-w-7xl mx-auto">
          {/* Outcomes List */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-semibold mb-3">{title}</h2>
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
                  <div className="flex-shrink-0 w-7 h-7 rounded-full bg-[#f7931a]/18 border border-[#f7931a]/40 flex items-center justify-center shadow-[0_10px_22px_rgba(247,147,26,0.25)] group-hover:bg-[#f7931a]/28 transition-colors">
                    <Check className="w-4 h-4 text-[#f7931a]" strokeWidth={2.4} />
                  </div>
                  <p className="text-zinc-200 text-lg leading-relaxed group-hover:text-white transition-colors">
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
