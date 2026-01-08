import { motion } from 'motion/react';
import { Linkedin, Mail, Shield } from 'lucide-react';

interface FooterProps {
  language: 'de' | 'en';
  onAdminClick?: () => void;
}

const translations = {
  de: {
    tagline: 'Einfachheit trifft Innovation',
    rights: 'Alle Rechte vorbehalten.',
    contact: 'Kontakt',
    legal: 'Rechtliches',
    privacy: 'Datenschutz',
    imprint: 'Impressum',
  },
  en: {
    tagline: 'Simplicity meets Innovation',
    rights: 'All rights reserved.',
    contact: 'Contact',
    legal: 'Legal',
    privacy: 'Privacy',
    imprint: 'Imprint',
  },
};

export function Footer({ language, onAdminClick }: FooterProps) {
  const t = translations[language];

  return (
    <footer className="bg-background border-t border-border py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-primary-foreground">D</span>
              </div>
              <span className="tracking-wider">DATALIZATION</span>
            </div>
            <p className="text-muted-foreground text-sm">{t.tagline}</p>
          </div>

          {/* Contact */}
          <div>
            <h4 className="mb-4">{t.contact}</h4>
            <div className="space-y-2">
              <a
                href="mailto:info@datalization.ch"
                className="flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors text-sm"
              >
                <Mail className="w-4 h-4" />
                info@datalization.ch
              </a>
              <a
                href="#"
                className="flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors text-sm"
              >
                <Linkedin className="w-4 h-4" />
                LinkedIn
              </a>
            </div>
          </div>

          {/* Legal */}
          <div>
            <h4 className="mb-4">{t.legal}</h4>
            <div className="space-y-2">
              <a href="#" className="block text-muted-foreground hover:text-primary transition-colors text-sm">
                {t.privacy}
              </a>
              <a href="#" className="block text-muted-foreground hover:text-primary transition-colors text-sm">
                {t.imprint}
              </a>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-border text-center text-muted-foreground text-sm">
          <p>© {new Date().getFullYear()} Datalization. {t.rights}</p>
          
          {/* Admin Access Button - Small and discreet */}
          {onAdminClick && (
            <button
              onClick={onAdminClick}
              className="inline-flex items-center gap-1 mt-4 px-3 py-1.5 text-xs text-zinc-600 hover:text-[#f7931a] transition-colors group"
              title="Admin Login"
            >
              <Shield className="w-3 h-3 group-hover:scale-110 transition-transform" />
              <span className="opacity-50 group-hover:opacity-100 transition-opacity">Admin</span>
            </button>
          )}
        </div>
      </div>
    </footer>
  );
}