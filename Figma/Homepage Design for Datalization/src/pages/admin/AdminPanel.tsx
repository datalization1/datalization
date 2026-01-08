import { useState } from 'react';
import { Login } from './Login';
import { AdminLayout } from './AdminLayout';
import { Dashboard } from './Dashboard';
import { ContactRequests } from './ContactRequests';
import { CaseStudiesManager } from './CaseStudiesManager';
import { CustomersManager } from './CustomersManager';
import { ContentManager } from './ContentManager';

export function AdminPanel() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentSection, setCurrentSection] = useState('dashboard');

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    if (confirm('Möchten Sie sich wirklich abmelden?')) {
      setIsAuthenticated(false);
      setCurrentSection('dashboard');
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  const renderSection = () => {
    switch (currentSection) {
      case 'dashboard':
        return <Dashboard onNavigate={setCurrentSection} />;
      case 'contacts':
        return <ContactRequests />;
      case 'cases':
        return <CaseStudiesManager />;
      case 'customers':
        return <CustomersManager />;
      case 'content':
        return <ContentManager />;
      default:
        return <Dashboard onNavigate={setCurrentSection} />;
    }
  };

  return (
    <AdminLayout
      currentSection={currentSection}
      onNavigate={setCurrentSection}
      onLogout={handleLogout}
    >
      {renderSection()}
    </AdminLayout>
  );
}
