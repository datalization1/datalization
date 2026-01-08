import { motion } from 'motion/react';
import { LucideIcon } from 'lucide-react';

interface ProcessStep {
  icon: LucideIcon;
  title: string;
  description: string;
}

interface ProcessSectionProps {
  title: string;
  subtitle?: string;
  steps: ProcessStep[];
}

export function ProcessSection({ title, subtitle, steps }: ProcessSectionProps) {
  return (
    <section className="py-20 bg-zinc-900/50 relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-transparent to-zinc-950 pointer-events-none" />

      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl mb-4">{title}</h2>
          {subtitle && (
            <p className="text-zinc-400 text-lg max-w-2xl mx-auto">{subtitle}</p>
          )}
        </motion.div>

        <div className="max-w-5xl mx-auto">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="relative mb-8 last:mb-0"
              >
                {/* Connection Line */}
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute left-8 top-20 w-0.5 h-[calc(100%+2rem)] bg-gradient-to-b from-[#f7931a]/30 to-transparent" />
                )}

                <div className="flex gap-6 items-start">
                  {/* Step Number & Icon */}
                  <div className="flex-shrink-0 relative">
                    <div className="w-16 h-16 bg-gradient-to-br from-[#f7931a] to-[#f7931a]/80 rounded-2xl flex items-center justify-center shadow-lg shadow-[#f7931a]/30 relative z-10">
                      <Icon className="w-8 h-8 text-zinc-950" />
                    </div>
                    <div className="absolute -top-2 -right-2 w-8 h-8 bg-zinc-900 border-2 border-[#f7931a] rounded-full flex items-center justify-center text-sm font-bold text-[#f7931a] z-20">
                      {index + 1}
                    </div>
                  </div>

                  {/* Content */}
                  <div className="flex-1 bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 hover:border-[#f7931a]/30 transition-all duration-300 group">
                    <h3 className="text-xl md:text-2xl mb-2 group-hover:text-[#f7931a] transition-colors">
                      {step.title}
                    </h3>
                    <p className="text-zinc-400 group-hover:text-zinc-300 transition-colors">
                      {step.description}
                    </p>
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
