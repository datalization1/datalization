import { motion } from 'motion/react';
import { useState } from 'react';
import { Mail, MessageSquare, User, Send } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { toast } from 'sonner@2.0.3';

interface ContactProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Kontakt',
    subtitle: 'Lassen Sie uns Ihre Vision gemeinsam verwirklichen',
    namePlaceholder: 'Ihr Name',
    emailPlaceholder: 'Ihre E-Mail',
    messagePlaceholder: 'Ihre Nachricht...',
    send: 'Nachricht senden',
    sending: 'Wird gesendet...',
    success: 'Vielen Dank! Wir melden uns bald bei Ihnen.',
    error: 'Bitte füllen Sie alle Felder aus.',
    info: 'Oder kontaktieren Sie uns direkt',
  },
  en: {
    title: 'Contact',
    subtitle: 'Let\'s realize your vision together',
    namePlaceholder: 'Your Name',
    emailPlaceholder: 'Your Email',
    messagePlaceholder: 'Your Message...',
    send: 'Send Message',
    sending: 'Sending...',
    success: 'Thank you! We\'ll get back to you soon.',
    error: 'Please fill in all fields.',
    info: 'Or contact us directly',
  },
};

export function Contact({ language }: ContactProps) {
  const t = translations[language];
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.message) {
      toast.error(t.error);
      return;
    }

    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      toast.success(t.success);
      setFormData({ name: '', email: '', message: '' });
      setIsSubmitting(false);
    }, 1500);
  };

  return (
    <section id="contact" className="py-24 bg-secondary/50 scroll-mt-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4">{t.title}</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">{t.subtitle}</p>
        </motion.div>

        <div className="max-w-2xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-card border border-border rounded-2xl p-8 md:p-12"
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="relative">
                <User className="absolute left-3 top-3.5 w-5 h-5 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder={t.namePlaceholder}
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="pl-12 bg-input-background border-border"
                />
              </div>

              <div className="relative">
                <Mail className="absolute left-3 top-3.5 w-5 h-5 text-muted-foreground" />
                <Input
                  type="email"
                  placeholder={t.emailPlaceholder}
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="pl-12 bg-input-background border-border"
                />
              </div>

              <div className="relative">
                <MessageSquare className="absolute left-3 top-3.5 w-5 h-5 text-muted-foreground" />
                <Textarea
                  placeholder={t.messagePlaceholder}
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  rows={6}
                  className="pl-12 bg-input-background border-border resize-none"
                />
              </div>

              <Button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground gap-2"
              >
                {isSubmitting ? (
                  t.sending
                ) : (
                  <>
                    {t.send}
                    <Send className="w-4 h-4" />
                  </>
                )}
              </Button>
            </form>

            <div className="mt-8 pt-8 border-t border-border text-center">
              <p className="text-muted-foreground mb-4">{t.info}</p>
              <a
                href="mailto:info@datalization.ch"
                className="text-primary hover:underline inline-flex items-center gap-2"
              >
                <Mail className="w-4 h-4" />
                info@datalization.ch
              </a>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
