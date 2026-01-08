import { motion } from 'motion/react';
import { ArrowRight, Download } from 'lucide-react';

interface CTASectionProps {
  title: string;
  description: string;
  primaryCTA: {
    text: string;
    onClick: () => void;
  };
  secondaryCTA?: {
    text: string;
    onClick: () => void;
  };
  downloadPDF?: {
    text: string;
    filename: string;
  };
}

export function CTASection({ title, description, primaryCTA, secondaryCTA, downloadPDF }: CTASectionProps) {
  return (
    <section className="py-20 bg-zinc-950 relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#f7931a]/10 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto text-center"
        >
          {/* Main Content */}
          <h2 className="text-3xl md:text-5xl mb-6">{title}</h2>
          <p className="text-xl text-zinc-400 mb-10 max-w-2xl mx-auto">
            {description}
          </p>

          {/* CTAs */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <button
              onClick={primaryCTA.onClick}
              className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium text-lg"
            >
              {primaryCTA.text}
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>

            {secondaryCTA && (
              <button
                onClick={secondaryCTA.onClick}
                className="inline-flex items-center gap-2 px-8 py-4 border border-zinc-700 rounded-full hover:border-[#f7931a]/50 hover:bg-[#f7931a]/5 transition-all duration-300 text-lg"
              >
                {secondaryCTA.text}
              </button>
            )}
          </div>

          {/* Download PDF */}
          {downloadPDF && (
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
            >
              <button
                onClick={() => {
                  // Mock PDF download
                  console.log(`Downloading ${downloadPDF.filename}`);
                }}
                className="inline-flex items-center gap-2 text-[#f7931a] hover:text-[#f7931a]/80 transition-colors group"
              >
                <Download className="w-4 h-4 group-hover:translate-y-0.5 transition-transform" />
                <span className="underline">{downloadPDF.text}</span>
              </button>
            </motion.div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
