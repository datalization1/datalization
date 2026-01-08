import { motion } from 'motion/react';
import { LucideIcon } from 'lucide-react';

interface Example {
  icon: LucideIcon;
  industry: string;
  scenario: string;
}

interface ExamplesSectionProps {
  title: string;
  subtitle?: string;
  examples: Example[];
}

export function ExamplesSection({ title, subtitle, examples }: ExamplesSectionProps) {
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

        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {examples.map((example, index) => {
            const Icon = example.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="group relative"
              >
                {/* Card */}
                <div className="relative bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 hover:border-[#f7931a]/50 transition-all duration-300 h-full">
                  {/* Hover Gradient */}
                  <div className="absolute inset-0 bg-gradient-to-br from-[#f7931a]/0 to-[#f7931a]/0 group-hover:from-[#f7931a]/5 group-hover:to-transparent rounded-xl transition-all duration-300" />

                  <div className="relative z-10">
                    {/* Icon */}
                    <div className="w-12 h-12 bg-[#f7931a]/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-[#f7931a]/20 transition-colors">
                      <Icon className="w-6 h-6 text-[#f7931a]" />
                    </div>

                    {/* Industry Badge */}
                    <div className="inline-block px-3 py-1 bg-[#f7931a]/10 rounded-full mb-3">
                      <span className="text-sm text-[#f7931a] font-medium">{example.industry}</span>
                    </div>

                    {/* Scenario */}
                    <p className="text-zinc-300 group-hover:text-white transition-colors">
                      {example.scenario}
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
