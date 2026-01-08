import { motion } from 'motion/react';
import { Mail, Phone, MapPin, Send } from 'lucide-react';
import { useForm } from 'react-hook-form@7.55.0';
import { toast } from 'sonner@2.0.3';

interface ContactPageProps {
  language: 'de' | 'en';
}

const translations = {
  de: {
    title: 'Kontakt',
    subtitle: 'Lassen Sie uns gemeinsam Ihre digitale Zukunft gestalten',
    formTitle: 'Schreiben Sie uns',
    formDescription: 'Füllen Sie das Formular aus und wir melden uns innerhalb von 24 Stunden bei Ihnen.',
    name: 'Name',
    namePlaceholder: 'Ihr Name',
    email: 'E-Mail',
    emailPlaceholder: 'ihre@email.com',
    phone: 'Telefon',
    phonePlaceholder: '+41 XX XXX XX XX',
    service: 'Gewünschter Service',
    servicePlaceholder: 'Wählen Sie einen Service',
    message: 'Nachricht',
    messagePlaceholder: 'Beschreiben Sie Ihr Projekt oder Ihre Anfrage...',
    submit: 'Nachricht senden',
    sending: 'Wird gesendet...',
    success: 'Nachricht erfolgreich gesendet!',
    error: 'Fehler beim Senden. Bitte versuchen Sie es erneut.',
    required: 'Dieses Feld ist erforderlich',
    invalidEmail: 'Ungültige E-Mail-Adresse',
    services: [
      'Datenanalyse & Data Science',
      'Softwareentwicklung',
      'Digitalisierung',
      'Beratung & Strategie',
      'Sonstiges',
    ],
    contactInfo: 'Kontaktinformationen',
    emailLabel: 'E-Mail',
    phoneLabel: 'Telefon',
    locationLabel: 'Standort',
    emailValue: 'info@datalization.ch',
    phoneValue: '+41 XX XXX XX XX',
    locationValue: 'Schweiz',
  },
  en: {
    title: 'Contact',
    subtitle: 'Let\'s shape your digital future together',
    formTitle: 'Get in Touch',
    formDescription: 'Fill out the form and we\'ll get back to you within 24 hours.',
    name: 'Name',
    namePlaceholder: 'Your Name',
    email: 'Email',
    emailPlaceholder: 'your@email.com',
    phone: 'Phone',
    phonePlaceholder: '+41 XX XXX XX XX',
    service: 'Desired Service',
    servicePlaceholder: 'Select a service',
    message: 'Message',
    messagePlaceholder: 'Describe your project or inquiry...',
    submit: 'Send Message',
    sending: 'Sending...',
    success: 'Message sent successfully!',
    error: 'Error sending message. Please try again.',
    required: 'This field is required',
    invalidEmail: 'Invalid email address',
    services: [
      'Data Analysis & Data Science',
      'Software Development',
      'Digitalization',
      'Consulting & Strategy',
      'Other',
    ],
    contactInfo: 'Contact Information',
    emailLabel: 'Email',
    phoneLabel: 'Phone',
    locationLabel: 'Location',
    emailValue: 'info@datalization.ch',
    phoneValue: '+41 XX XXX XX XX',
    locationValue: 'Switzerland',
  },
};

export function ContactPage({ language }: ContactPageProps) {
  const t = translations[language];
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm();

  const onSubmit = async (data: any) => {
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      console.log('Form data:', data);
      toast.success(t.success);
      reset();
    } catch (error) {
      toast.error(t.error);
    }
  };

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
            className="text-center mb-16"
          >
            <h1 className="text-5xl md:text-6xl mb-6">{t.title}</h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">{t.subtitle}</p>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <div className="bg-card border border-border rounded-2xl p-8">
                <h2 className="text-3xl mb-2">{t.formTitle}</h2>
                <p className="text-muted-foreground mb-8">{t.formDescription}</p>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                  {/* Name */}
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium mb-2">
                      {t.name}
                    </label>
                    <input
                      id="name"
                      type="text"
                      {...register('name', { required: t.required })}
                      placeholder={t.namePlaceholder}
                      className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f7931a] focus:border-transparent transition-all"
                    />
                    {errors.name && (
                      <p className="text-red-400 text-sm mt-1">{errors.name.message as string}</p>
                    )}
                  </div>

                  {/* Email */}
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium mb-2">
                      {t.email}
                    </label>
                    <input
                      id="email"
                      type="email"
                      {...register('email', {
                        required: t.required,
                        pattern: {
                          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                          message: t.invalidEmail,
                        },
                      })}
                      placeholder={t.emailPlaceholder}
                      className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f7931a] focus:border-transparent transition-all"
                    />
                    {errors.email && (
                      <p className="text-red-400 text-sm mt-1">{errors.email.message as string}</p>
                    )}
                  </div>

                  {/* Phone */}
                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium mb-2">
                      {t.phone}
                    </label>
                    <input
                      id="phone"
                      type="tel"
                      {...register('phone')}
                      placeholder={t.phonePlaceholder}
                      className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f7931a] focus:border-transparent transition-all"
                    />
                  </div>

                  {/* Service */}
                  <div>
                    <label htmlFor="service" className="block text-sm font-medium mb-2">
                      {t.service}
                    </label>
                    <select
                      id="service"
                      {...register('service')}
                      className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f7931a] focus:border-transparent transition-all appearance-none cursor-pointer"
                    >
                      <option value="">{t.servicePlaceholder}</option>
                      {t.services.map((service) => (
                        <option key={service} value={service}>
                          {service}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Message */}
                  <div>
                    <label htmlFor="message" className="block text-sm font-medium mb-2">
                      {t.message}
                    </label>
                    <textarea
                      id="message"
                      {...register('message', { required: t.required })}
                      rows={6}
                      placeholder={t.messagePlaceholder}
                      className="w-full px-4 py-3 bg-zinc-900/50 border border-zinc-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f7931a] focus:border-transparent transition-all resize-none"
                    />
                    {errors.message && (
                      <p className="text-red-400 text-sm mt-1">{errors.message.message as string}</p>
                    )}
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                  >
                    {isSubmitting ? (
                      <>
                        <div className="w-5 h-5 border-2 border-zinc-950 border-t-transparent rounded-full animate-spin" />
                        {t.sending}
                      </>
                    ) : (
                      <>
                        <Send className="w-5 h-5" />
                        {t.submit}
                      </>
                    )}
                  </button>
                </form>
              </div>
            </motion.div>

            {/* Contact Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="space-y-8"
            >
              <div className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-2xl p-8">
                <h2 className="text-3xl mb-6">{t.contactInfo}</h2>
                
                <div className="space-y-6">
                  {/* Email */}
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center flex-shrink-0">
                      <Mail className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="text-lg mb-1">{t.emailLabel}</h3>
                      <a
                        href={`mailto:${t.emailValue}`}
                        className="text-muted-foreground hover:text-primary transition-colors"
                      >
                        {t.emailValue}
                      </a>
                    </div>
                  </div>

                  {/* Phone */}
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center flex-shrink-0">
                      <Phone className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="text-lg mb-1">{t.phoneLabel}</h3>
                      <a
                        href={`tel:${t.phoneValue}`}
                        className="text-muted-foreground hover:text-primary transition-colors"
                      >
                        {t.phoneValue}
                      </a>
                    </div>
                  </div>

                  {/* Location */}
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center flex-shrink-0">
                      <MapPin className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="text-lg mb-1">{t.locationLabel}</h3>
                      <p className="text-muted-foreground">{t.locationValue}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Additional Info Card */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 }}
                className="bg-card border border-border rounded-2xl p-8"
              >
                <h3 className="text-xl mb-4 text-primary">
                  {language === 'de' ? 'Warum Datalization?' : 'Why Datalization?'}
                </h3>
                <ul className="space-y-3 text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <span className="text-primary mt-1">✓</span>
                    <span>
                      {language === 'de'
                        ? 'Individuelle Lösungen für Ihre Bedürfnisse'
                        : 'Custom solutions for your needs'}
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary mt-1">✓</span>
                    <span>
                      {language === 'de'
                        ? 'Transparente Kommunikation und Prozesse'
                        : 'Transparent communication and processes'}
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary mt-1">✓</span>
                    <span>
                      {language === 'de'
                        ? 'Langfristige Partnerschaften'
                        : 'Long-term partnerships'}
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary mt-1">✓</span>
                    <span>
                      {language === 'de'
                        ? 'Moderne Technologien und Best Practices'
                        : 'Modern technologies and best practices'}
                    </span>
                  </li>
                </ul>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>
    </main>
  );
}
