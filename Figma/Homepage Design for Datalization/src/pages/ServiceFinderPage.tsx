import { ServiceFinder } from '../components/ServiceFinder';

interface ServiceFinderPageProps {
  language: 'de' | 'en';
  onServiceClick: (serviceId: string) => void;
  scrollToContact: () => void;
}

export function ServiceFinderPage({ language, onServiceClick, scrollToContact }: ServiceFinderPageProps) {
  return (
    <div className="min-h-screen bg-zinc-950 text-white pt-20">
      <ServiceFinder 
        language={language} 
        onServiceClick={onServiceClick}
        scrollToContact={scrollToContact}
      />
    </div>
  );
}
