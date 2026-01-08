import { useState, useEffect } from 'react';
import { Navigation } from './components/Navigation';
import { Hero } from './components/Hero';
import { QuickCheckCTA } from './components/home/QuickCheckCTA';
import { Vision } from './components/Vision';
import { Approach } from './components/Approach';
import { Services } from './components/Services';
import { CaseStudies } from './components/CaseStudies';
import { About } from './components/About';
import { Contact } from './components/Contact';
import { Footer } from './components/Footer';
import { ServiceFinderPage } from './pages/ServiceFinderPage';
import { AboutPage } from './pages/AboutPage';
import { ContactPage } from './pages/ContactPage';
import { CaseStudiesPage } from './pages/CaseStudiesPage';
import { DataAnalytics } from './pages/services/DataAnalytics';
import { Software } from './pages/services/Software';
import { Digitalization } from './pages/services/Digitalization';
import { Consulting } from './pages/services/Consulting';
import { AdminPanel } from './pages/admin/AdminPanel';
import { Toaster } from './components/ui/sonner';

type Page = 'home' | 'about' | 'contact' | 'case-studies' | 'service-finder' | 'data-analytics' | 'software' | 'digitalization' | 'consulting' | 'admin';

export default function App() {
  // Detect browser language and set default
  const getBrowserLanguage = (): 'de' | 'en' => {
    const browserLang = navigator.language.toLowerCase();
    // If browser language starts with 'de', use German, otherwise English
    return browserLang.startsWith('de') ? 'de' : 'en';
  };

  const [language, setLanguage] = useState<'de' | 'en'>(getBrowserLanguage());
  const [currentPage, setCurrentPage] = useState<Page>('home');

  // Check URL for admin access
  useEffect(() => {
    const path = window.location.pathname;
    if (path === '/admin' || path.includes('/admin')) {
      setCurrentPage('admin');
    }
  }, []);

  const scrollToContact = () => {
    if (currentPage !== 'home') {
      setCurrentPage('home');
      setTimeout(() => {
        document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Scroll to top when changing pages
  const handlePageChange = (page: Page | string) => {
    setCurrentPage(page as Page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Admin Panel
  if (currentPage === 'admin') {
    return (
      <>
        <AdminPanel />
        <Toaster />
      </>
    );
  }

  // Service Finder Page
  if (currentPage === 'service-finder') {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <ServiceFinderPage 
          language={language} 
          onServiceClick={(serviceId: string) => handlePageChange(serviceId)}
          scrollToContact={scrollToContact}
        />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  // Service Detail Pages
  if (currentPage === 'data-analytics') {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <DataAnalytics 
          language={language} 
          onContact={scrollToContact}
          onNavigateToFinder={() => handlePageChange('service-finder')}
        />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  if (currentPage === 'software') {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <Software 
          language={language} 
          onContact={scrollToContact}
          onNavigateToFinder={() => handlePageChange('service-finder')}
        />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  if (currentPage === 'digitalization') {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <Digitalization 
          language={language} 
          onContact={scrollToContact}
          onNavigateToFinder={() => handlePageChange('service-finder')}
        />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  if (currentPage === 'consulting') {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <Consulting 
          language={language} 
          onContact={scrollToContact}
          onNavigateToFinder={() => handlePageChange('service-finder')}
        />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  // About Page
  if (currentPage === 'about') {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <AboutPage language={language} />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  // Contact Page
  if (currentPage === 'contact') {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <ContactPage language={language} />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  // Case Studies Page
  if (currentPage === 'case-studies') {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
          onServiceClick={handlePageChange}
          onAboutClick={() => handlePageChange('about')}
          onContactClick={() => handlePageChange('contact')}
          onCaseStudiesClick={() => handlePageChange('case-studies')}
        />
        <CaseStudiesPage language={language} />
        <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
        <Toaster />
      </div>
    );
  }

  // Home Page
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation 
        language={language} 
        setLanguage={setLanguage}
        onLogoClick={() => handlePageChange('home')}
        currentPage={currentPage}
        onServiceClick={handlePageChange}
        onAboutClick={() => handlePageChange('about')}
        onContactClick={() => handlePageChange('contact')}
        onCaseStudiesClick={() => handlePageChange('case-studies')}
      />
      <Hero language={language} />
      <QuickCheckCTA 
        language={language} 
        onNavigate={() => handlePageChange('service-finder')}
      />
      <Vision language={language} />
      <Approach language={language} />
      <Services 
        language={language} 
        onServiceClick={(serviceId: string) => {
          handlePageChange(serviceId);
        }} 
      />
      <CaseStudies language={language} />
      <About language={language} />
      <Contact language={language} />
      <Footer language={language} onAdminClick={() => handlePageChange('admin')} />
      <Toaster />
    </div>
  );
}