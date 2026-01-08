import { motion } from 'motion/react';
import { Lightbulb, Compass, Sparkles } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface AboutProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Über uns',
    subtitle: 'Wer wir sind',
    intro: 'Datalization ist mehr als nur ein Unternehmen - es ist eine Vision für eine digitale Zukunft, in der Komplexität durch Einfachheit ersetzt wird.',
    story: 'Geboren aus der Überzeugung, dass Technologie dem Menschen dienen sollte und nicht umgekehrt, schaffen wir Lösungen, die nicht nur funktionieren, sondern begeistern. Wie der Jaguar - frei, flexibel und kraftvoll - bewegen wir uns durch die digitale Landschaft mit Geschwindigkeit und Präzision.',
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
    commitment: 'Unser Versprechen',
    commitmentText: 'Wir setzen nicht auf schnelle Erfolge, sondern auf nachhaltige Partnerschaften. Loyal zu unseren Werten, loyal zu unseren Kunden - das ist der Datalization-Weg.',
  },
  en: {
    title: 'About Us',
    subtitle: 'Who we are',
    intro: 'Datalization is more than just a company - it\'s a vision for a digital future where complexity is replaced by simplicity.',
    story: 'Born from the conviction that technology should serve people and not vice versa, we create solutions that not only work but inspire. Like the jaguar - free, flexible and powerful - we move through the digital landscape with speed and precision.',
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
    commitment: 'Our Promise',
    commitmentText: 'We don\'t focus on quick wins, but on sustainable partnerships. Loyal to our values, loyal to our customers - that\'s the Datalization way.',
  },
};

export function About({ language }: AboutProps) {
  const t = translations[language];

  return (
    <section id="about" className="py-24 scroll-mt-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4">{t.title}</h2>
          <p className="text-muted-foreground">{t.subtitle}</p>
        </motion.div>

        <div className="max-w-4xl mx-auto mb-16">
          {/* Team/Collaboration Image */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-12 rounded-2xl overflow-hidden"
          >
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1758518731457-5ef826b75b3b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjB0ZWFtJTIwY29sbGFib3JhdGlvbnxlbnwxfHx8fDE3Njc4MTExOTV8MA&ixlib=rb-4.1.0&q=80&w=1080"
              alt="Team collaboration"
              className="w-full h-96 object-cover"
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-2xl p-8 md:p-12 mb-8"
          >
            <p className="text-xl mb-6">{t.intro}</p>
            <p className="text-muted-foreground">{t.story}</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 mb-12">
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
  );
}