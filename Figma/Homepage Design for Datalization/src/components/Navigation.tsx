import { useState } from 'react';
import { Menu, X, Globe, ChevronDown } from 'lucide-react';
import { Button } from './ui/button';
import logo from 'figma:asset/9c79fd0c49d5bb3ae17428ccf646e5ea86915053.png';

interface NavigationProps {
  language: 'de' | 'en';
  setLanguage: (lang: 'de' | 'en') => void;
  onLogoClick?: () => void;
  currentPage?: string;
  onServiceClick?: (serviceId: string) => void;
  onAboutClick?: () => void;
  onContactClick?: () => void;
  onCaseStudiesClick?: () => void;
}

const translations = {
  de: {
    services: 'Lösungen',
    cases: 'Case Studies',
    about: 'Über uns',
    contact: 'Kontakt',
    serviceFinder: 'Was passt zu mir?',
    servicesDropdown: {
      dataAnalytics: 'Datenanalyse & Data Science',
      software: 'Softwareentwicklung',
      digitalization: 'Digitalisierung',
      consulting: 'Beratung & Strategie',
    },
  },
  en: {
    services: 'Solutions',
    cases: 'Case Studies',
    about: 'About',
    contact: 'Contact',
    serviceFinder: 'What fits for me?',
    servicesDropdown: {
      dataAnalytics: 'Data Analytics & Data Science',
      software: 'Software Development',
      digitalization: 'Digitalization',
      consulting: 'Consulting & Strategy',
    },
  },
};

export function Navigation({ language, setLanguage, onLogoClick, currentPage, onServiceClick, onAboutClick, onContactClick, onCaseStudiesClick }: NavigationProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [servicesDropdownOpen, setServicesDropdownOpen] = useState(false);
  const [mobileServicesOpen, setMobileServicesOpen] = useState(false);
  const t = translations[language];

  const handleCaseStudiesClick = () => {
    if (onCaseStudiesClick) {
      onCaseStudiesClick();
      setMobileMenuOpen(false);
    }
  };

  const scrollToSection = (id: string) => {
    // If not on home page, navigate home first
    if (currentPage !== 'home') {
      if (onLogoClick) {
        onLogoClick();
        setTimeout(() => {
          const element = document.getElementById(id);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
          }
        }, 100);
      }
    } else {
      const element = document.getElementById(id);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
        setMobileMenuOpen(false);
      }
    }
  };

  const handleServiceClick = (serviceId: string) => {
    if (onServiceClick) {
      onServiceClick(serviceId);
      setServicesDropdownOpen(false);
      setMobileMenuOpen(false);
      setMobileServicesOpen(false);
    }
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-zinc-950/95 backdrop-blur-sm border-b border-zinc-800">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <button 
            onClick={onLogoClick}
            className="flex items-center gap-3 hover:opacity-80 transition-opacity"
          >
            <img src={logo} alt="datalization" className="w-10 h-10" />
            <span className="text-white lowercase tracking-wide text-xl">datalization</span>
          </button>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            {/* Services Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setServicesDropdownOpen(true)}
              onMouseLeave={() => setServicesDropdownOpen(false)}
            >
              <button
                className="flex items-center gap-1 hover:text-[#f7931a] transition-colors py-2"
              >
                {t.services}
                <ChevronDown className={`w-4 h-4 transition-transform ${servicesDropdownOpen ? 'rotate-180' : ''}`} />
              </button>
              
              {servicesDropdownOpen && (
                <div className="absolute left-0 top-full pt-1 w-80">
                  <div className="bg-zinc-900/95 backdrop-blur-sm border border-zinc-800 rounded-xl shadow-2xl shadow-black/50 overflow-hidden">
                    <div className="py-2">
                      <button
                        onClick={() => handleServiceClick('data-analytics')}
                        className="w-full px-6 py-3 text-left hover:bg-[#f7931a]/10 hover:text-[#f7931a] transition-all group"
                      >
                        <div className="text-sm font-medium">{t.servicesDropdown.dataAnalytics}</div>
                      </button>
                      <button
                        onClick={() => handleServiceClick('software')}
                        className="w-full px-6 py-3 text-left hover:bg-[#f7931a]/10 hover:text-[#f7931a] transition-all group"
                      >
                        <div className="text-sm font-medium">{t.servicesDropdown.software}</div>
                      </button>
                      <button
                        onClick={() => handleServiceClick('digitalization')}
                        className="w-full px-6 py-3 text-left hover:bg-[#f7931a]/10 hover:text-[#f7931a] transition-all group"
                      >
                        <div className="text-sm font-medium">{t.servicesDropdown.digitalization}</div>
                      </button>
                      <button
                        onClick={() => handleServiceClick('consulting')}
                        className="w-full px-6 py-3 text-left hover:bg-[#f7931a]/10 hover:text-[#f7931a] transition-all group"
                      >
                        <div className="text-sm font-medium">{t.servicesDropdown.consulting}</div>
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <button onClick={handleCaseStudiesClick} className="hover:text-[#f7931a] transition-colors">
              {t.cases}
            </button>
            <button onClick={onAboutClick} className="hover:text-[#f7931a] transition-colors">
              {t.about}
            </button>
            <button onClick={onContactClick} className="hover:text-[#f7931a] transition-colors">
              {t.contact}
            </button>
            
            {/* Service Finder Button - Orange CTA */}
            <button
              onClick={() => handleServiceClick('service-finder')}
              className="px-4 py-2 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/90 text-zinc-950 rounded-lg hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 hover:scale-105 font-medium"
            >
              {t.serviceFinder}
            </button>
            
            {/* Language Switcher Dropdown */}
            <div className="relative group">
              <button className="flex items-center gap-2 px-3 py-2 border border-zinc-700 rounded-lg hover:border-[#f7931a]/50 transition-colors">
                <Globe className="w-4 h-4" />
                <span>{language.toUpperCase()}</span>
                <ChevronDown className="w-3 h-3" />
              </button>
              
              <div className="absolute right-0 top-full mt-2 w-32 bg-zinc-900/95 backdrop-blur-sm border border-zinc-800 rounded-lg shadow-2xl shadow-black/50 overflow-hidden opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                <button
                  onClick={() => setLanguage('de')}
                  className={`w-full px-4 py-2 text-left text-sm hover:bg-[#f7931a]/10 transition-colors ${language === 'de' ? 'text-[#f7931a]' : ''}`}
                >
                  Deutsch
                </button>
                <button
                  onClick={() => setLanguage('en')}
                  className={`w-full px-4 py-2 text-left text-sm hover:bg-[#f7931a]/10 transition-colors ${language === 'en' ? 'text-[#f7931a]' : ''}`}
                >
                  English
                </button>
              </div>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pb-4 flex flex-col gap-3">
            {/* Service Finder Button - Mobile */}
            <button
              onClick={() => handleServiceClick('service-finder')}
              className="px-4 py-2.5 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/90 text-zinc-950 rounded-lg hover:shadow-lg hover:shadow-[#f7931a]/50 transition-all duration-300 font-medium text-center"
            >
              {t.serviceFinder}
            </button>
            
            {/* Mobile Services Dropdown */}
            <div>
              <button 
                onClick={() => setMobileServicesOpen(!mobileServicesOpen)}
                className="w-full flex items-center justify-between text-left hover:text-[#f7931a] transition-colors"
              >
                <span>{t.services}</span>
                <ChevronDown className={`w-4 h-4 transition-transform ${mobileServicesOpen ? 'rotate-180' : ''}`} />
              </button>
              
              {mobileServicesOpen && (
                <div className="mt-2 ml-4 flex flex-col gap-2 border-l-2 border-zinc-800 pl-4">
                  <button
                    onClick={() => handleServiceClick('data-analytics')}
                    className="text-left text-sm text-zinc-400 hover:text-[#f7931a] transition-colors"
                  >
                    {t.servicesDropdown.dataAnalytics}
                  </button>
                  <button
                    onClick={() => handleServiceClick('software')}
                    className="text-left text-sm text-zinc-400 hover:text-[#f7931a] transition-colors"
                  >
                    {t.servicesDropdown.software}
                  </button>
                  <button
                    onClick={() => handleServiceClick('digitalization')}
                    className="text-left text-sm text-zinc-400 hover:text-[#f7931a] transition-colors"
                  >
                    {t.servicesDropdown.digitalization}
                  </button>
                  <button
                    onClick={() => handleServiceClick('consulting')}
                    className="text-left text-sm text-zinc-400 hover:text-[#f7931a] transition-colors"
                  >
                    {t.servicesDropdown.consulting}
                  </button>
                </div>
              )}
            </div>
            
            <button onClick={handleCaseStudiesClick} className="text-left hover:text-[#f7931a] transition-colors">
              {t.cases}
            </button>
            <button onClick={onAboutClick} className="text-left hover:text-[#f7931a] transition-colors">
              {t.about}
            </button>
            <button onClick={onContactClick} className="text-left hover:text-[#f7931a] transition-colors">
              {t.contact}
            </button>
            
            {/* Mobile Language Switcher */}
            <div className="pt-3 border-t border-zinc-800 flex gap-2">
              <button
                onClick={() => setLanguage('de')}
                className={`flex-1 px-4 py-2 rounded-lg border transition-colors ${
                  language === 'de' 
                    ? 'border-[#f7931a] bg-[#f7931a]/10 text-[#f7931a]' 
                    : 'border-zinc-700 hover:border-zinc-600'
                }`}
              >
                Deutsch
              </button>
              <button
                onClick={() => setLanguage('en')}
                className={`flex-1 px-4 py-2 rounded-lg border transition-colors ${
                  language === 'en' 
                    ? 'border-[#f7931a] bg-[#f7931a]/10 text-[#f7931a]' 
                    : 'border-zinc-700 hover:border-zinc-600'
                }`}
              >
                English
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}