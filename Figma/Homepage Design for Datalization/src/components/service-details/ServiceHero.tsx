import { motion } from 'motion/react';
import { ArrowRight } from 'lucide-react';

interface ServiceHeroProps {
  headline: string;
  subline: string;
  visual?: React.ReactNode;
  onPrimaryCTA: () => void;
  onSecondaryCTA?: () => void;
  primaryCTAText: string;
  secondaryCTAText?: string;
}

export function ServiceHero({
  headline,
  subline,
  visual,
  onPrimaryCTA,
  onSecondaryCTA,
  primaryCTAText,
  secondaryCTAText,
}: ServiceHeroProps) {
  return (
    <section className="relative py-32 bg-zinc-950 overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-[#f7931a]/10 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center max-w-7xl mx-auto">
          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl md:text-6xl mb-6 leading-tight">
              {headline}
            </h1>
            <p className="text-xl text-zinc-400 mb-8 leading-relaxed">
              {subline}
            </p>

            <div className="flex flex-wrap gap-4">
              <button
                onClick={onPrimaryCTA}
                className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium"
              >
                {primaryCTAText}
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>

              {secondaryCTAText && onSecondaryCTA && (
                <button
                  onClick={onSecondaryCTA}
                  className="inline-flex items-center gap-2 px-8 py-4 border border-zinc-700 rounded-full hover:border-[#f7931a]/50 hover:bg-[#f7931a]/5 transition-all duration-300"
                >
                  {secondaryCTAText}
                </button>
              )}
            </div>
          </motion.div>

          {/* Visual */}
          {visual && (
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
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
