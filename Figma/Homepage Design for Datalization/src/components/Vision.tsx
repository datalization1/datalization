import { motion } from 'motion/react';
import { Heart, Target, Zap } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface VisionProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Unsere Vision',
    vision: 'Loyal leben und einfache Lösungen schaffen',
    values: [
      {
        icon: Heart,
        title: 'Loyalität',
        description: 'Wir stehen zu unseren Werten und bauen langfristige Partnerschaften auf Vertrauen.',
      },
      {
        icon: Zap,
        title: 'Einfachheit',
        description: 'Komplexität reduzieren, Klarheit schaffen - das ist unsere Mission.',
      },
      {
        icon: Target,
        title: 'Innovation',
        description: 'Mit zukunftsorientierten Lösungen Ihre digitale Transformation gestalten.',
      },
    ],
  },
  en: {
    title: 'Our Vision',
    vision: 'Live loyally and create simple solutions',
    values: [
      {
        icon: Heart,
        title: 'Loyalty',
        description: 'We stand by our values and build long-term partnerships based on trust.',
      },
      {
        icon: Zap,
        title: 'Simplicity',
        description: 'Reducing complexity, creating clarity - that\'s our mission.',
      },
      {
        icon: Target,
        title: 'Innovation',
        description: 'Shaping your digital transformation with forward-thinking solutions.',
      },
    ],
  },
};

export function Vision({ language }: VisionProps) {
  const t = translations[language];

  return (
    <section className="py-24 bg-zinc-900/50 relative overflow-hidden">
      {/* Background gradient effect */}
      <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-transparent to-zinc-950 pointer-events-none" />
      
      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-6">{t.title}</h2>
          <p className="text-2xl text-[#f7931a] max-w-3xl mx-auto">
            {t.vision}
          </p>
        </motion.div>

        {/* Abstract Technology Image */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="mb-16 max-w-4xl mx-auto rounded-2xl overflow-hidden"
        >
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1762279389042-9439bfb6c155?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjB0ZWNobm9sb2d5JTIwYWJzdHJhY3R8ZW58MXx8fHwxNzY3ODg0MzA3fDA&ixlib=rb-4.1.0&q=80&w=1080"
            alt="Modern Technology"
            className="w-full h-80 object-cover opacity-80"
          />
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {t.values.map((value, index) => {
            const Icon = value.icon;
            return (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="relative group"
              >
                {/* Glassmorphism Card */}
                <div className="relative bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-8 hover:border-[#f7931a]/50 transition-all duration-300 hover:shadow-lg hover:shadow-[#f7931a]/10">
                  {/* Hover Gradient Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-br from-[#f7931a]/0 to-[#f7931a]/0 group-hover:from-[#f7931a]/5 group-hover:to-transparent rounded-2xl transition-all duration-300" />
                  
                  <div className="relative z-10">
                    <div className="w-16 h-16 bg-[#f7931a]/10 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-[#f7931a]/20 transition-all duration-300 group-hover:scale-110 transform">
                      <Icon className="w-8 h-8 text-[#f7931a]" />
                    </div>
                    <h3 className="text-2xl mb-4 group-hover:text-[#f7931a] transition-colors duration-300">{value.title}</h3>
                    <p className="text-zinc-400 group-hover:text-zinc-300 transition-colors duration-300">{value.description}</p>
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