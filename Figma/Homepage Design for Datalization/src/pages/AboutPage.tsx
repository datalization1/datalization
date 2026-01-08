import { motion } from 'motion/react';
import { Lightbulb, Compass, Sparkles, Heart, Target, Zap, Users, Award, TrendingUp } from 'lucide-react';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

interface AboutPageProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Über uns',
    subtitle: 'Wer wir sind und wofür wir stehen',
    intro: 'Datalization ist mehr als nur ein Unternehmen - es ist eine Vision für eine digitale Zukunft, in der Komplexität durch Einfachheit ersetzt wird.',
    story: 'Geboren aus der Überzeugung, dass Technologie dem Menschen dienen sollte und nicht umgekehrt, schaffen wir Lösungen, die nicht nur funktionieren, sondern begeistern. Wie der Jaguar - frei, flexibel und kraftvoll - bewegen wir uns durch die digitale Landschaft mit Geschwindigkeit und Präzision.',
    visionTitle: 'Unsere Vision',
    visionText: 'Loyal leben und einfache Lösungen schaffen',
    principles: [
      {
        icon: Compass,
        title: 'Freiheit',
        description: 'Unabhängige Lösungen, die Sie nicht einschränken, sondern befähigen.',
      },
      {
        icon: Sparkles,
        title: 'Flexibilität',
        description: 'Anpassungsfähige Systeme, die mit Ihrem Unternehmen wachsen.',
      },
      {
        icon: Lightbulb,
        title: 'Klarheit',
        description: 'Transparente Prozesse und verständliche Ergebnisse.',
      },
    ],
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
    commitment: 'Unser Versprechen',
    commitmentText: 'Wir setzen nicht auf schnelle Erfolge, sondern auf nachhaltige Partnerschaften. Loyal zu unseren Werten, loyal zu unseren Kunden - das ist der Datalization-Weg.',
    stats: [
      {
        icon: Users,
        value: '50+',
        label: 'Zufriedene Kunden',
      },
      {
        icon: Award,
        value: '100+',
        label: 'Erfolgreiche Projekte',
      },
      {
        icon: TrendingUp,
        value: '5+',
        label: 'Jahre Erfahrung',
      },
    ],
  },
  en: {
    title: 'About Us',
    subtitle: 'Who we are and what we stand for',
    intro: 'Datalization is more than just a company - it\'s a vision for a digital future where complexity is replaced by simplicity.',
    story: 'Born from the conviction that technology should serve people and not vice versa, we create solutions that not only work but inspire. Like the jaguar - free, flexible and powerful - we move through the digital landscape with speed and precision.',
    visionTitle: 'Our Vision',
    visionText: 'Live loyally and create simple solutions',
    principles: [
      {
        icon: Compass,
        title: 'Freedom',
        description: 'Independent solutions that don\'t restrict you, but empower you.',
      },
      {
        icon: Sparkles,
        title: 'Flexibility',
        description: 'Adaptive systems that grow with your business.',
      },
      {
        icon: Lightbulb,
        title: 'Clarity',
        description: 'Transparent processes and understandable results.',
      },
    ],
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
    commitment: 'Our Promise',
    commitmentText: 'We don\'t focus on quick wins, but on sustainable partnerships. Loyal to our values, loyal to our customers - that\'s the Datalization way.',
    stats: [
      {
        icon: Users,
        value: '50+',
        label: 'Satisfied Clients',
      },
      {
        icon: Award,
        value: '100+',
        label: 'Successful Projects',
      },
      {
        icon: TrendingUp,
        value: '5+',
        label: 'Years Experience',
      },
    ],
  },
};

export function AboutPage({ language }: AboutPageProps) {
  const t = translations[language];

  return (
    <main className="min-h-screen pt-24">
      {/* Hero Section */}
      <section className="py-16 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-[#f7931a]/5 via-transparent to-transparent pointer-events-none" />
        
        <div className="container mx-auto px-4 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h1 className="text-5xl md:text-6xl mb-6">{t.title}</h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">{t.subtitle}</p>
          </motion.div>

          {/* Team/Collaboration Image */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mb-16 max-w-5xl mx-auto rounded-2xl overflow-hidden"
          >
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1758518731457-5ef826b75b3b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjB0ZWFtJTIwY29sbGFib3JhdGlvbnxlbnwxfHx8fDE3Njc4MTExOTV8MA&ixlib=rb-4.1.0&q=80&w=1080"
              alt="Team collaboration"
              className="w-full h-96 object-cover"
            />
          </motion.div>
        </div>
      </section>

      {/* Story Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-2xl p-8 md:p-12 mb-12"
            >
              <p className="text-xl mb-6">{t.intro}</p>
              <p className="text-muted-foreground">{t.story}</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-zinc-900/50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {t.stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-primary" />
                  </div>
                  <div className="text-4xl font-bold text-primary mb-2">{stat.value}</div>
                  <p className="text-muted-foreground">{stat.label}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Vision Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl mb-6">{t.visionTitle}</h2>
            <p className="text-2xl text-[#f7931a] max-w-3xl mx-auto">
              {t.visionText}
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
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
                  <div className="relative bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-8 hover:border-[#f7931a]/50 transition-all duration-300 hover:shadow-lg hover:shadow-[#f7931a]/10">
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

      {/* Principles Section */}
      <section className="py-16 bg-zinc-900/50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto mb-12">
            {t.principles.map((principle, index) => {
              const Icon = principle.icon;
              return (
                <motion.div
                  key={principle.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-primary" />
                  </div>
                  <h3 className="text-xl mb-2">{principle.title}</h3>
                  <p className="text-muted-foreground text-sm">{principle.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Commitment Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="bg-card border border-border rounded-2xl p-8 text-center"
            >
              <h3 className="text-2xl mb-4 text-primary">{t.commitment}</h3>
              <p className="text-muted-foreground">{t.commitmentText}</p>
            </motion.div>
          </div>
        </div>
      </section>
    </main>
  );
}
