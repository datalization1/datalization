import { motion } from 'motion/react';
import { Package, LucideIcon } from 'lucide-react';

interface Deliverable {
  icon?: LucideIcon;
  title: string;
  description?: string;
}

interface DeliverablesSectionProps {
  title: string;
  subtitle?: string;
  deliverables: Deliverable[];
}

export function DeliverablesSection({ title, subtitle, deliverables }: DeliverablesSectionProps) {
  return (
    <section className="py-20 bg-zinc-900/30">
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

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {deliverables.map((deliverable, index) => {
            const Icon = deliverable.icon || Package;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
                className="group"
              >
                <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-6 hover:border-[#f7931a]/50 hover:shadow-lg hover:shadow-[#f7931a]/10 transition-all duration-300 h-full">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-10 h-10 bg-[#f7931a]/10 rounded-lg flex items-center justify-center group-hover:bg-[#f7931a]/20 transition-colors">
                      <Icon className="w-5 h-5 text-[#f7931a]" />
                    </div>
                    <div>
                      <h3 className="text-lg font-medium mb-1 group-hover:text-[#f7931a] transition-colors">
                        {deliverable.title}
                      </h3>
                      {deliverable.description && (
                        <p className="text-sm text-zinc-400 group-hover:text-zinc-300 transition-colors">
                          {deliverable.description}
                        </p>
                      )}
                    </div>
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
