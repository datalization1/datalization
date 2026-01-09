import { motion } from 'motion/react';
import { Linkedin, Mail, Shield } from 'lucide-react';

interface FooterProps {
  language: 'de' | 'en';
  onAdminClick?: () => void;
  onNavigate?: (page: string) => void;
}

const translations = {
  de: {
    tagline: 'Einfachheit trifft Innovation',
    rights: 'Alle Rechte vorbehalten.',
    services: 'Services',
    dataAnalytics: 'Data Analytics & Data Science',
    software: 'Softwareentwicklung',
    digitalization: 'Digitalisierung',
    consulting: 'Beratung & Strategie',
    company: 'Unternehmen',
    about: 'Über uns',
    caseStudies: 'Case Studies',
    contact: 'Kontakt',
    tools: 'Tools',
    serviceFinder: 'Was passt zu mir?',
    connect: 'Kontakt',
    legal: 'Rechtliches',
    privacy: 'Datenschutz',
    imprint: 'Impressum',
  },
  en: {
    tagline: 'Simplicity meets Innovation',
    rights: 'All rights reserved.',
    services: 'Services',
    dataAnalytics: 'Data Analytics & Data Science',
    software: 'Software Development',
    digitalization: 'Digitalization',
    consulting: 'Consulting & Strategy',
    company: 'Company',
    about: 'About Us',
    caseStudies: 'Case Studies',
    contact: 'Contact',
    tools: 'Tools',
    serviceFinder: 'What fits your needs?',
    connect: 'Connect',
    legal: 'Legal',
    privacy: 'Privacy',
    imprint: 'Imprint',
  },
};

export function Footer({ language, onAdminClick, onNavigate }: FooterProps) {
  const t = translations[language];

  const handleNavigation = (page: string) => {
    if (onNavigate) {
      onNavigate(page);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <footer className="bg-zinc-950 border-t border-zinc-800 py-16">
      <div className="container mx-auto px-4">
        {/* Main Footer Content */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-12 gap-8 mb-12">
          {/* Brand */}
          <div className="col-span-2 md:col-span-4 lg:col-span-4">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-[#f7931a] to-[#f7931a]/80 rounded-lg flex items-center justify-center">
                <span className="text-zinc-950 font-bold text-lg">D</span>
              </div>
              <span className="text-xl tracking-wider font-medium">DATALIZATION</span>
            </div>
            <p className="text-zinc-400 text-sm mb-4 max-w-xs">{t.tagline}</p>
            <p className="text-zinc-500 text-xs">
              Loyal leben und einfache Lösungen schaffen
            </p>
          </div>

          {/* Services */}
          <div className="lg:col-span-3">
            <h4 className="font-medium mb-4 text-white">{t.services}</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleNavigation('data-analytics')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.dataAnalytics}
              </button>
              <button
                onClick={() => handleNavigation('software')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.software}
              </button>
              <button
                onClick={() => handleNavigation('digitalization')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.digitalization}
              </button>
              <button
                onClick={() => handleNavigation('consulting')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.consulting}
              </button>
            </div>
          </div>

          {/* Company */}
          <div className="lg:col-span-2">
            <h4 className="font-medium mb-4 text-white">{t.company}</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleNavigation('about')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.about}
              </button>
              <button
                onClick={() => handleNavigation('case-studies')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.caseStudies}
              </button>
              <button
                onClick={() => handleNavigation('contact')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.contact}
              </button>
            </div>
          </div>

          {/* Tools */}
          <div className="lg:col-span-2">
            <h4 className="font-medium mb-4 text-white">{t.tools}</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleNavigation('service-finder')}
                className="block text-zinc-400 hover:text-[#f7931a] transition-colors text-sm text-left"
              >
                {t.serviceFinder}
              </button>
            </div>
          </div>

          {/* Contact */}
          <div className="col-span-2 md:col-span-2 lg:col-span-1">
            <h4 className="font-medium mb-4 text-white">{t.connect}</h4>
            <div className="space-y-3">
              <a
                href="mailto:info@datalization.ch"
                className="flex items-center gap-2 text-zinc-400 hover:text-[#f7931a] transition-colors text-sm group"
              >
                <Mail className="w-4 h-4 group-hover:scale-110 transition-transform" />
                info@datalization.ch
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-zinc-400 hover:text-[#f7931a] transition-colors text-sm group"
              >
                <Linkedin className="w-4 h-4 group-hover:scale-110 transition-transform" />
                LinkedIn
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-zinc-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-zinc-500 text-sm">
              © {new Date().getFullYear()} Datalization. {t.rights}
            </p>
            
            {/* Legal Links */}
            <div className="flex items-center gap-6">
              <a href="#" className="text-zinc-500 hover:text-[#f7931a] transition-colors text-sm">
                {t.privacy}
              </a>
              <a href="#" className="text-zinc-500 hover:text-[#f7931a] transition-colors text-sm">
                {t.imprint}
              </a>
              
              {/* Admin Access Button - Small and discreet */}
              {onAdminClick && (
                <button
                  onClick={onAdminClick}
                  className="inline-flex items-center gap-1 px-3 py-1.5 text-xs text-zinc-600 hover:text-[#f7931a] transition-colors group"
                  title="Admin Login"
                >
                  <Shield className="w-3 h-3 group-hover:scale-110 transition-transform" />
                  <span className="opacity-50 group-hover:opacity-100 transition-opacity">Admin</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}