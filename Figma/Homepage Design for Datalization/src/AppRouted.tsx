import { useState } from 'react';
import { Navigation } from './components/Navigation';
import { Hero } from './components/Hero';
import { Vision } from './components/Vision';
import { Approach } from './components/Approach';
import { Services } from './components/Services';
import { CaseStudies } from './components/CaseStudies';
import { About } from './components/About';
import { Contact } from './components/Contact';
import { Footer } from './components/Footer';
import { DataAnalytics } from './pages/services/DataAnalytics';
import { Toaster } from './components/ui/sonner';

type Page = 'home' | 'data-analytics' | 'software' | 'digitalization' | 'consulting';

export default function AppRouted() {
  const [language, setLanguage] = useState<'de' | 'en'>('de');
  const [currentPage, setCurrentPage] = useState<Page>('home');

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
  const handlePageChange = (page: Page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (currentPage === 'data-analytics') {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navigation 
          language={language} 
          setLanguage={setLanguage}
          onLogoClick={() => handlePageChange('home')}
          currentPage={currentPage}
        />
        <DataAnalytics language={language} onContact={scrollToContact} />
        <Footer language={language} />
        <Toaster />
      </div>
    );
  }

  // Home page
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation 
        language={language} 
        setLanguage={setLanguage}
        onLogoClick={() => handlePageChange('home')}
        currentPage={currentPage}
      />
      <Hero language={language} />
      <Vision language={language} />
      <Approach language={language} />
      <Services language={language} onServiceClick={(serviceId: string) => {
        if (serviceId === 'data-analytics') {
          handlePageChange('data-analytics');
        }
        // Add other services later
      }} />
      <CaseStudies language={language} />
      <About language={language} />
      <Contact language={language} />
      <Footer language={language} />
      <Toaster />
    </div>
  );
}
