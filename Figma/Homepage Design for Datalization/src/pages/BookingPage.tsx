import { motion } from 'motion/react';
import { Calendar, Clock, CheckCircle, ArrowRight, Mail, Phone } from 'lucide-react';
import { useState } from 'react';
import { toast } from 'sonner@2.0.3';

interface BookingPageProps {
  language: 'de' | 'en';
  serviceType?: 'data-analytics' | 'software' | 'digitalization' | 'consulting';
}

const translations = {
  de: {
    title: 'Kurz-Check buchen',
    subtitle: 'Kostenloses 20-Minuten Gespräch',
    description: 'Buchen Sie jetzt Ihren persönlichen Kurz-Check. Wir schauen gemeinsam, ob und wie unsere Leistungen zu Ihren Bedürfnissen passen.',
    benefits: {
      title: 'Was Sie erwartet:',
      items: [
        'Kostenlos & unverbindlich',
        '20 Minuten persönliches Gespräch',
        'Konkrete Einschätzung Ihrer Situation',
        'Erste Lösungsansätze & nächste Schritte',
        'Keine versteckten Kosten',
      ],
    },
    form: {
      title: 'Ihre Kontaktdaten',
      name: 'Vor- und Nachname',
      namePlaceholder: 'Max Mustermann',
      email: 'E-Mail',
      emailPlaceholder: 'max@beispiel.ch',
      phone: 'Telefon (optional)',
      phonePlaceholder: '+41 79 123 45 67',
      company: 'Firma (optional)',
      companyPlaceholder: 'Ihre Firma',
      service: 'Interessiert an',
      serviceOptions: {
        general: 'Allgemeine Beratung',
        dataAnalytics: 'Data Analytics & Data Science',
        software: 'Softwareentwicklung',
        digitalization: 'Digitalisierung',
        consulting: 'Beratung & Strategie',
      },
      message: 'Ihre Situation (optional)',
      messagePlaceholder: 'Beschreiben Sie kurz Ihre aktuelle Herausforderung...',
      preferredDate: 'Wunschtermin (optional)',
      preferredTime: 'Bevorzugte Uhrzeit',
      timeOptions: {
        morning: 'Vormittags (9-12 Uhr)',
        afternoon: 'Nachmittags (12-17 Uhr)',
        evening: 'Abends (17-20 Uhr)',
      },
      submit: 'Jetzt Kurz-Check buchen',
      submitting: 'Wird gesendet...',
    },
    privacy: 'Mit dem Absenden stimmen Sie der Verarbeitung Ihrer Daten gemäß unserer Datenschutzerklärung zu.',
    success: {
      title: 'Anfrage erfolgreich!',
      message: 'Wir melden uns innerhalb von 24 Stunden bei Ihnen, um einen Termin zu vereinbaren.',
    },
    howItWorks: {
      title: 'So funktioniert\'s',
      steps: [
        {
          icon: Calendar,
          title: 'Formular ausfüllen',
          description: 'Teilen Sie uns Ihre Kontaktdaten und Ihren Wunschtermin mit.',
        },
        {
          icon: Mail,
          title: 'Terminbestätigung',
          description: 'Wir melden uns innerhalb von 24h mit Terminvorschlägen.',
        },
        {
          icon: Clock,
          title: '20-Min Gespräch',
          description: 'Persönliches Gespräch per Telefon, Videocall oder vor Ort.',
        },
        {
          icon: CheckCircle,
          title: 'Nächste Schritte',
          description: 'Sie erhalten konkrete Empfehlungen für Ihre Situation.',
        },
      ],
    },
  },
  en: {
    title: 'Book Quick Check',
    subtitle: 'Free 20-Minute Consultation',
    description: 'Book your personal quick check now. We\'ll look together at whether and how our services fit your needs.',
    benefits: {
      title: 'What to expect:',
      items: [
        'Free & non-binding',
        '20-minute personal conversation',
        'Concrete assessment of your situation',
        'First solution approaches & next steps',
        'No hidden costs',
      ],
    },
    form: {
      title: 'Your Contact Details',
      name: 'Full Name',
      namePlaceholder: 'John Doe',
      email: 'Email',
      emailPlaceholder: 'john@example.com',
      phone: 'Phone (optional)',
      phonePlaceholder: '+41 79 123 45 67',
      company: 'Company (optional)',
      companyPlaceholder: 'Your Company',
      service: 'Interested in',
      serviceOptions: {
        general: 'General Consulting',
        dataAnalytics: 'Data Analytics & Data Science',
        software: 'Software Development',
        digitalization: 'Digitalization',
        consulting: 'Consulting & Strategy',
      },
      message: 'Your Situation (optional)',
      messagePlaceholder: 'Briefly describe your current challenge...',
      preferredDate: 'Preferred Date (optional)',
      preferredTime: 'Preferred Time',
      timeOptions: {
        morning: 'Morning (9am-12pm)',
        afternoon: 'Afternoon (12pm-5pm)',
        evening: 'Evening (5pm-8pm)',
      },
      submit: 'Book Quick Check Now',
      submitting: 'Sending...',
    },
    privacy: 'By submitting, you agree to the processing of your data according to our privacy policy.',
    success: {
      title: 'Request successful!',
      message: 'We\'ll get back to you within 24 hours to schedule an appointment.',
    },
    howItWorks: {
      title: 'How it works',
      steps: [
        {
          icon: Calendar,
          title: 'Fill out form',
          description: 'Share your contact details and preferred date with us.',
        },
        {
          icon: Mail,
          title: 'Appointment confirmation',
          description: 'We\'ll contact you within 24h with appointment suggestions.',
        },
        {
          icon: Clock,
          title: '20-min conversation',
          description: 'Personal talk via phone, video call, or in person.',
        },
        {
          icon: CheckCircle,
          title: 'Next steps',
          description: 'You\'ll receive concrete recommendations for your situation.',
        },
      ],
    },
  },
};

export function BookingPage({ language, serviceType }: BookingPageProps) {
  const t = translations[language];
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    service: serviceType || 'general',
    message: '',
    preferredDate: '',
    preferredTime: 'morning',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    console.log('Booking submitted:', formData);
    toast.success(language === 'de' ? 'Anfrage erfolgreich gesendet!' : 'Request sent successfully!');
    setSubmitted(true);
    setIsSubmitting(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-zinc-950 text-white pt-32 pb-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="max-w-2xl mx-auto text-center"
          >
            <div className="w-20 h-20 bg-gradient-to-br from-[#f7931a] to-[#f7931a]/80 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-10 h-10 text-zinc-950" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">{t.success.title}</h1>
            <p className="text-xl text-zinc-400 mb-8">{t.success.message}</p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => setSubmitted(false)}
                className="px-6 py-3 bg-zinc-800 hover:bg-zinc-700 rounded-full transition-colors"
              >
                {language === 'de' ? 'Zurück' : 'Back'}
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white pt-32 pb-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-3xl mx-auto text-center mb-16"
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-4">{t.title}</h1>
          <p className="text-xl md:text-2xl text-[#f7931a] mb-6">{t.subtitle}</p>
          <p className="text-lg text-zinc-400">{t.description}</p>
        </motion.div>

        <div className="max-w-6xl mx-auto grid lg:grid-cols-3 gap-12">
          {/* Left Column: Benefits & How it Works */}
          <div className="lg:col-span-1 space-y-8">
            {/* Benefits */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-6"
            >
              <h3 className="text-xl font-bold mb-4">{t.benefits.title}</h3>
              <ul className="space-y-3">
                {t.benefits.items.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-[#f7931a] flex-shrink-0 mt-0.5" />
                    <span className="text-zinc-300">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>

            {/* How it Works */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-6"
            >
              <h3 className="text-xl font-bold mb-6">{t.howItWorks.title}</h3>
              <div className="space-y-6">
                {t.howItWorks.steps.map((step, index) => {
                  const Icon = step.icon;
                  return (
                    <div key={index} className="flex gap-4">
                      <div className="w-10 h-10 bg-gradient-to-br from-[#f7931a] to-[#f7931a]/80 rounded-full flex items-center justify-center flex-shrink-0">
                        <Icon className="w-5 h-5 text-zinc-950" />
                      </div>
                      <div>
                        <h4 className="font-medium mb-1">{step.title}</h4>
                        <p className="text-sm text-zinc-400">{step.description}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          </div>

          {/* Right Column: Form */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            <form onSubmit={handleSubmit} className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-8">
              <h3 className="text-2xl font-bold mb-6">{t.form.title}</h3>

              <div className="space-y-6">
                {/* Name */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    {t.form.name} <span className="text-[#f7931a]">*</span>
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder={t.form.namePlaceholder}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors"
                  />
                </div>

                {/* Email & Phone */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      {t.form.email} <span className="text-[#f7931a]">*</span>
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      placeholder={t.form.emailPlaceholder}
                      className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">{t.form.phone}</label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      placeholder={t.form.phonePlaceholder}
                      className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors"
                    />
                  </div>
                </div>

                {/* Company */}
                <div>
                  <label className="block text-sm font-medium mb-2">{t.form.company}</label>
                  <input
                    type="text"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    placeholder={t.form.companyPlaceholder}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors"
                  />
                </div>

                {/* Service */}
                <div>
                  <label className="block text-sm font-medium mb-2">
                    {t.form.service} <span className="text-[#f7931a]">*</span>
                  </label>
                  <select
                    name="service"
                    value={formData.service}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors"
                  >
                    <option value="general">{t.form.serviceOptions.general}</option>
                    <option value="data-analytics">{t.form.serviceOptions.dataAnalytics}</option>
                    <option value="software">{t.form.serviceOptions.software}</option>
                    <option value="digitalization">{t.form.serviceOptions.digitalization}</option>
                    <option value="consulting">{t.form.serviceOptions.consulting}</option>
                  </select>
                </div>

                {/* Message */}
                <div>
                  <label className="block text-sm font-medium mb-2">{t.form.message}</label>
                  <textarea
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    rows={4}
                    placeholder={t.form.messagePlaceholder}
                    className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors resize-none"
                  />
                </div>

                {/* Preferred Date & Time */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">{t.form.preferredDate}</label>
                    <input
                      type="date"
                      name="preferredDate"
                      value={formData.preferredDate}
                      onChange={handleChange}
                      className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">{t.form.preferredTime}</label>
                    <select
                      name="preferredTime"
                      value={formData.preferredTime}
                      onChange={handleChange}
                      className="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg focus:outline-none focus:border-[#f7931a] transition-colors"
                    >
                      <option value="morning">{t.form.timeOptions.morning}</option>
                      <option value="afternoon">{t.form.timeOptions.afternoon}</option>
                      <option value="evening">{t.form.timeOptions.evening}</option>
                    </select>
                  </div>
                </div>

                {/* Privacy Notice */}
                <p className="text-xs text-zinc-500">{t.privacy}</p>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="group w-full inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                >
                  {isSubmitting ? t.form.submitting : t.form.submit}
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
