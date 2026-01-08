# Datalization Website - Vollständige Dokumentation

## Inhaltsverzeichnis
1. [Projektübersicht](#projektübersicht)
2. [Technologie-Stack](#technologie-stack)
3. [Projektstruktur](#projektstruktur)
4. [Design-System](#design-system)
5. [Komponenten-Dokumentation](#komponenten-dokumentation)
6. [Seiten-Dokumentation](#seiten-dokumentation)
7. [Zweisprachigkeit](#zweisprachigkeit)
8. [Navigation & Routing](#navigation--routing)
9. [Features & Funktionalitäten](#features--funktionalitäten)
10. [Admin-Panel](#admin-panel)
11. [Deployment & Integration](#deployment--integration)

---

## Projektübersicht

### Über Datalization
**Datalization** ist eine Einzelunternehmung spezialisiert auf:
- Datenanalyse & Data Science
- Softwareentwicklung
- Digitalisierung
- Beratung & Strategie

### Vision
"Loyal leben und einfache Lösungen schaffen"

### Design-Philosophie
Inspiriert vom Jaguar-Design mit den Werten:
- **Freiheit**: Flexible und anpassbare Lösungen
- **Flexibilität**: Agile Methoden und moderne Technologien
- **Eleganz**: Minimalistisches, professionelles Design

---

## Technologie-Stack

### Frontend-Framework
- **React 18+** - Moderne UI-Bibliothek
- **TypeScript** - Type-sicherer JavaScript-Code
- **Vite** - Schneller Build-Tool und Dev-Server

### Styling
- **Tailwind CSS v4** - Utility-first CSS Framework
- **Glassmorphism** - Moderne UI-Effekte mit Backdrop-Blur
- **Motion/React** - Animationen und Transitions

### UI-Komponenten & Utilities
- **Lucide React** - Icon-Bibliothek
- **Sonner** - Toast-Notifications
- **React Hook Form 7.55.0** - Formular-Management
- **Recharts** - Daten-Visualisierung (falls benötigt)

### Backend-Integration (Django-ready)
- Alle Komponenten sind statisch und Django-Template-kompatibel
- Kein State-Management über Grenzen hinweg
- Alle API-Aufrufe können durch Django-Views ersetzt werden

---

## Projektstruktur

```
/
├── App.tsx                          # Haupt-App mit Routing-Logik
├── index.html                       # HTML-Einstiegspunkt
├── main.tsx                         # React-Einstiegspunkt
├── vite.config.ts                   # Vite-Konfiguration
│
├── /components                      # Wiederverwendbare Komponenten
│   ├── Navigation.tsx               # Hauptnavigation mit Dropdown
│   ├── Hero.tsx                     # Hero-Section Homepage
│   ├── Vision.tsx                   # Vision-Section
│   ├── Approach.tsx                 # Approach-Section
│   ├── Services.tsx                 # Services-Overview
│   ├── CaseStudies.tsx              # Case Studies Section
│   ├── About.tsx                    # About-Section
│   ├── Contact.tsx                  # Kontaktformular
│   ├── Footer.tsx                   # Footer
│   │
│   ├── /home                        # Homepage-spezifische Komponenten
│   │   └── QuickCheckCTA.tsx        # Quick-Check Call-to-Action (neu!)
│   │
│   ├── /service-details             # Service-Detail-Komponenten
│   │   ├── ServiceHero.tsx          # Hero für Service-Seiten
│   │   ├── QuickCheckButton.tsx     # Button zur Service-Finder-Seite (neu!)
│   │   ├── OutcomesSection.tsx      # Ergebnisse & Vorteile
│   │   ├── ProcessSection.tsx       # Prozess-Übersicht
│   │   ├── ExamplesSection.tsx      # Beispiele & Use Cases
│   │   ├── DeliverablesSection.tsx  # Deliverables-Liste
│   │   ├── FAQSection.tsx           # FAQ-Accordion
│   │   ├── CTASection.tsx           # Call-to-Action
│   │   └── StickyCTA.tsx            # Sticky CTA Button
│   │
│   ├── /ui                          # UI-Basiskomponenten
│   │   ├── button.tsx               # Button-Komponente
│   │   └── sonner.tsx               # Toast-Notifications
│   │
│   └── /figma                       # Figma-Import-Helper
│       └── ImageWithFallback.tsx    # Image-Komponente (geschützt)
│
├── /pages                           # Seiten-Komponenten
│   ├── ServiceFinderPage.tsx        # Service-Finder mit 3-Fragen-Check (neu!)
│   │
│   ├── /services                    # Service-Detailseiten
│   │   ├── DataAnalytics.tsx        # Datenanalyse-Seite
│   │   ├── Software.tsx             # Softwareentwicklung-Seite
│   │   ├── Digitalization.tsx       # Digitalisierung-Seite
│   │   └── Consulting.tsx           # Beratung & Strategie-Seite
│   │
│   └── /admin                       # Admin-Panel (8 Komponenten)
│       ├── AdminPanel.tsx           # Haupt-Komponente mit Routing
│       ├── Login.tsx                # Login-Seite
│       ├── AdminLayout.tsx          # Layout mit Sidebar
│       ├── Dashboard.tsx            # Dashboard mit Übersicht
│       ├── ContactRequests.tsx      # Kontaktanfragen-Verwaltung
│       ├── CaseStudiesManager.tsx   # Case Studies CRUD
│       ├── CustomersManager.tsx     # Kunden-Verwaltung
│       └── ContentManager.tsx       # Content Management System
│
└── /styles                          # Globale Styles
    └── globals.css                  # Tailwind-Setup & Custom-Styles
```

---

## Design-System

### Farbpalette

#### Primärfarben
- **Hintergrund**: `#09090b` (zinc-950)
- **Akzentfarbe**: `#f7931a` (Orange)
- **Text**: `#ffffff` (Weiß), `#a1a1aa` (zinc-400)

#### Graustufenpalette (Zinc)
- `zinc-950`: Haupthintergrund
- `zinc-900`: Cards, Dropdown-Hintergründe
- `zinc-800`: Borders, Dividers
- `zinc-700`: Sekundäre Borders
- `zinc-400`: Sekundärer Text

### Typografie
Definiert in `/styles/globals.css`:
- **Basis-Font**: System-Font-Stack
- **Headings**: Standard HTML-Elemente (h1, h2, h3, etc.)
- Keine manuellen Font-Größen in Komponenten (außer explizit gewünscht)

### Spacing & Layout
- **Container**: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Section-Padding**: `py-16 sm:py-20 lg:py-24`
- **Gap-System**: `gap-4, gap-6, gap-8, gap-12`

### Glassmorphism-Effekte
```css
/* Card-Stil */
bg-zinc-900/50 backdrop-blur-sm border border-zinc-800

/* Navigation */
bg-zinc-950/95 backdrop-blur-sm border-b border-zinc-800

/* Dropdown */
bg-zinc-900/95 backdrop-blur-sm border border-zinc-800
```

### Animationen & Transitions
- **Hover-Transitions**: `transition-colors`, `transition-opacity`, `transition-all`
- **Duration**: Standard Tailwind-Durations
- **Hover-Effekte**: 
  - Text: `hover:text-[#f7931a]`
  - Borders: `hover:border-[#f7931a]/50`
  - Backgrounds: `hover:bg-[#f7931a]/10`

---

## Komponenten-Dokumentation

### Navigation.tsx

**Zweck**: Hauptnavigation mit Dropdown-Menü für Services und Sprachumschalter

**Props**:
```typescript
interface NavigationProps {
  language: 'de' | 'en';
  setLanguage: (lang: 'de' | 'en') => void;
  onLogoClick?: () => void;
  currentPage?: string;
  onServiceClick?: (serviceId: string) => void;
}
```

**Features**:
- Sticky Navigation (fixed top)
- Service-Dropdown mit 4 Optionen
- Sprachumschalter (Desktop: Dropdown, Mobile: Buttons)
- Responsive Mobile-Menü
- Scroll-to-Section Funktion
- Service-Navigation

**Translations**:
- Deutsch/Englisch für alle Menüpunkte
- Service-Namen werden übersetzt

---

### Hero.tsx

**Zweck**: Hero-Section der Homepage mit Hauptbotschaft

**Props**:
```typescript
interface HeroProps {
  language: 'de' | 'en';
}
```

**Features**:
- Großer Titel mit Tagline
- CTA-Buttons (Kontakt + Mehr erfahren)
- Scroll-Indikator
- Responsive Design

**Translations**:
- Titel, Untertitel, Button-Texte

---

### Vision.tsx

**Zweck**: Vision-Statement der Firma

**Props**:
```typescript
interface VisionProps {
  language: 'de' | 'en';
}
```

**Features**:
- Zentraler Vision-Text
- Jaguar-Design-Werte (Freiheit & Flexibilität)
- Icon-basierte Darstellung

---

### Approach.tsx

**Zweck**: Darstellung der Arbeitsweise

**Props**:
```typescript
interface ApproachProps {
  language: 'de' | 'en';
}
```

**Features**:
- 3-4 Kernpunkte der Arbeitsweise
- Grid-Layout
- Icon + Text-Kombination

---

### Services.tsx

**Zweck**: Übersicht der 4 Hauptservices mit "Mehr erfahren"-Links

**Props**:
```typescript
interface ServicesProps {
  language: 'de' | 'en';
  onServiceClick: (serviceId: string) => void;
}
```

**Features**:
- 4 Service-Cards im Grid
- Glassmorphism-Effekte
- Hover-Animationen
- "Mehr erfahren"-Buttons führen zu Detail-Seiten

**Services**:
1. Datenanalyse & Data Science
2. Softwareentwicklung
3. Digitalisierung
4. Beratung & Strategie

---

### CaseStudies.tsx

**Zweck**: Darstellung von Projekt-Beispielen

**Props**:
```typescript
interface CaseStudiesProps {
  language: 'de' | 'en';
}
```

**Features**:
- Case Study Cards
- Projekt-Beschreibungen
- Technologie-Tags
- Ergebnisse/Erfolge

---

### About.tsx

**Zweck**: "Who we are" Section

**Props**:
```typescript
interface AboutProps {
  language: 'de' | 'en';
}
```

**Features**:
- Team/Firma-Vorstellung
- Werte und Philosophie
- Expertise-Bereiche

---

### Contact.tsx

**Zweck**: Kontaktformular mit Validierung

**Props**:
```typescript
interface ContactProps {
  language: 'de' | 'en';
}
```

**Features**:
- React Hook Form Integration
- Formular-Felder:
  - Name (required)
  - Email (required, validated)
  - Telefon (optional)
  - Nachricht (required)
  - Service-Auswahl (Dropdown)
- Client-seitige Validierung
- Toast-Notifications (Erfolg/Fehler)
- Mock-Submit (bereit für Django-Integration)

**Validierung**:
- Email-Format-Prüfung
- Pflichtfeld-Prüfung
- Min/Max-Length

---

### Footer.tsx

**Zweck**: Website-Footer mit Links und Infos

**Props**:
```typescript
interface FooterProps {
  language: 'de' | 'en';
  onServiceClick: (serviceId: string) => void;
}
```

**Features**:
- Service-Links
- Social Media Links (vorbereitet)
- Copyright-Hinweis
- Mehrspaltiges Layout (Desktop)

---

## Service-Detail-Komponenten

Alle Service-Detailseiten nutzen diese 8 wiederverwendbaren Komponenten:

### 1. ServiceHero.tsx

**Zweck**: Hero-Section für Service-Detailseiten

**Props**:
```typescript
interface ServiceHeroProps {
  title: string;
  subtitle: string;
  description: string;
  icon: React.ReactNode;
  stats?: Array<{
    value: string;
    label: string;
  }>;
}
```

**Features**:
- Service-Titel mit Icon
- Beschreibungstext
- Optional: Statistiken/Kennzahlen

---

### 2. QuickCheckButton.tsx

**Zweck**: Button zur Service-Finder-Seite (ersetzt den alten QuickCheck-Fragebogen)

**Props**:
```typescript
interface QuickCheckButtonProps {
  language: 'de' | 'en';
  onNavigate: () => void;
}
```

**Features**:
- Einfacher Button mit Icon
- Leitet direkt zur Service-Finder-Seite weiter
- Glassmorphism-Design
- Zweisprachig (DE/EN)
- Call-to-Action Text: "Welche Lösung passt zu mir?"

**Verwendung**:
- Ersetzt den komplexen interaktiven Fragebogen auf Service-Seiten
- Vereinfacht den User-Flow
- Zentralisiert die Service-Empfehlung auf einer dedizierten Seite

---

### 3. OutcomesSection.tsx

**Zweck**: Darstellung der Ergebnisse und Vorteile

**Props**:
```typescript
interface OutcomesSectionProps {
  title: string;
  outcomes: Array<{
    icon: React.ReactNode;
    title: string;
    description: string;
  }>;
}
```

**Features**:
- Grid-Layout (3 Spalten Desktop)
- Icon + Titel + Beschreibung
- Glassmorphism-Cards

---

### 4. ProcessSection.tsx

**Zweck**: Darstellung des Projekt-Prozesses

**Props**:
```typescript
interface ProcessSectionProps {
  title: string;
  steps: Array<{
    number: string;
    title: string;
    description: string;
  }>;
}
```

**Features**:
- Nummerierte Schritte
- Timeline-Design
- Mobile-optimiert (vertical layout)

---

### 5. ExamplesSection.tsx

**Zweck**: Use-Cases und Beispiel-Projekte

**Props**:
```typescript
interface ExamplesSectionProps {
  title: string;
  examples: Array<{
    title: string;
    description: string;
    tags: string[];
  }>;
}
```

**Features**:
- Beispiel-Cards
- Technologie-Tags
- 2-Spalten-Grid (Desktop)

---

### 6. DeliverablesSection.tsx

**Zweck**: Übersicht der Projekt-Deliverables

**Props**:
```typescript
interface DeliverablesSectionProps {
  title: string;
  deliverables: Array<{
    icon: React.ReactNode;
    title: string;
    items: string[];
  }>;
}
```

**Features**:
- Kategorisierte Deliverables
- Aufzählungslisten
- Icons für Kategorien

---

### 7. FAQSection.tsx

**Zweck**: Häufig gestellte Fragen (Accordion)

**Props**:
```typescript
interface FAQSectionProps {
  title: string;
  faqs: Array<{
    question: string;
    answer: string;
  }>;
}
```

**Features**:
- Accordion-UI (expand/collapse)
- Smooth-Transitions
- ChevronDown-Animation
- Click-to-expand

---

### 8. CTASection.tsx

**Zweck**: Call-to-Action am Seitenende

**Props**:
```typescript
interface CTASectionProps {
  title: string;
  description: string;
  buttonText: string;
  onButtonClick: () => void;
}
```

**Features**:
- Zentrale CTA-Box
- Glassmorphism-Design
- Großer Button

---

### 9. StickyCTA.tsx

**Zweck**: Sticky-Button am unteren Bildschirmrand

**Props**:
```typescript
interface StickyCTAProps {
  text: string;
  onClick: () => void;
}
```

**Features**:
- Fixed Position (bottom)
- Erscheint nach Scroll
- Mobile-optimiert
- Orange Highlight

---

## Seiten-Dokumentation

### Homepage (App.tsx - currentPage: 'home')

**Komponenten-Reihenfolge**:
1. Navigation
2. Hero
3. QuickCheckCTA (neu! - "Welche Lösung passt zu mir?")
4. Vision
5. Approach
6. Services
7. CaseStudies
8. About
9. Contact
10. Footer

**ID-Anchors für Scroll-Navigation**:
- `#services`
- `#cases`
- `#about`
- `#contact`

---

### Service-Finder-Seite (ServiceFinderPage.tsx - currentPage: 'service-finder')

**Zweck**: Dedizierte Seite für den interaktiven 3-Fragen-Check zur Service-Empfehlung

**Datei**: `/pages/ServiceFinderPage.tsx`

**Props**:
```typescript
interface ServiceFinderPageProps {
  language: 'de' | 'en';
  onServiceClick: (serviceId: string) => void;
  scrollToContact: () => void;
}
```

**Features**:

**1. Hero-Section**:
- Titel: "Finden Sie die perfekte Lösung"
- Untertitel mit Schritten-Erklärung
- Sparkles-Icon
- Glow-Effekt

**2. Interaktiver 3-Fragen-Check**:
- **Frage 1**: Hauptziel (4 Optionen)
  - Daten analysieren und visualisieren → Datenanalyse
  - Software entwickeln → Softwareentwicklung
  - Prozesse digitalisieren → Digitalisierung
  - Strategie entwickeln → Beratung

- **Frage 2**: Größtes Problem (4 Optionen)
  - Daten nicht nutzbar
  - Manuelle repetitive Aufgaben
  - Veraltete Systeme
  - Unklare Digitalisierungsstrategie

- **Frage 3**: Wichtigste Anforderung (4 Optionen)
  - Daten-getriebene Entscheidungen
  - Automatisierung von Prozessen
  - Nahtlose Systemintegration
  - Langfristige strategische Planung

**3. Service-Empfehlung**:
- Automatische Empfehlung basierend auf Antworten
- Empfehlungs-Card mit:
  - Service-Icon
  - Service-Name
  - Beschreibung
  - "Mehr erfahren"-Button → Service-Detail-Seite
- Alternative Services werden angezeigt

**4. Empfehlungs-Logik**:
```typescript
// Scoring-System für jede Frage
question1: {
  'analyze': 'data-analytics',
  'develop': 'software',
  'digitize': 'digitalization',
  'strategy': 'consulting'
}
// Mehrheit der Antworten bestimmt Empfehlung
```

**5. Call-to-Action**:
- "Noch unsicher?"-Section
- Button: "Kontakt aufnehmen"
- Scroll zur Kontakt-Section auf Homepage

**Design**:
- Glassmorphism-Cards
- Motion-Animationen
- Progressive Disclosure (Fragen nacheinander)
- Orange Akzente (#f7931a)
- Responsive Layout

**User-Flow**:
1. Benutzer landet auf Service-Finder
2. Beantwortet 3 Multiple-Choice-Fragen
3. Erhält automatische Service-Empfehlung
4. Kann direkt zur Service-Detailseite navigieren
5. Oder Kontakt aufnehmen

---

### Home-Komponenten

#### QuickCheckCTA.tsx

**Zweck**: Call-to-Action auf der Startseite zur Service-Finder-Seite

**Datei**: `/components/home/QuickCheckCTA.tsx`

**Props**:
```typescript
interface QuickCheckCTAProps {
  language: 'de' | 'en';
  onNavigate: () => void;
}
```

**Features**:
- **Sparkles-Icon**: Große orangene Sparkles in rundem Hintergrund
- **Hauptfrage**: "Welche Lösung passt zu mir?" (DE) / "Which solution is right for me?" (EN)
- **Untertitel**: "Machen Sie unseren 3-Fragen-Check und finden Sie es heraus"
- **CTA-Button**: Großer orangener Button → Service-Finder-Seite
- **Glow-Effekt**: Subtiler Hintergrund-Glow
- **Animations**: Motion-Animationen beim Scroll-in

**Platzierung**:
- Direkt **nach dem Hero-Teil** auf der Startseite
- Vor Vision, Approach und Services
- Prominente Positionierung für maximale Sichtbarkeit

**Design**:
- Zentriertes Layout
- Dunkler Hintergrund (zinc-950)
- Orange Akzente
- Hover-Effekte auf Button
- Responsive (Mobile & Desktop)

**Translations**:
```typescript
de: {
  title: 'Welche Lösung passt zu mir?',
  subtitle: 'Machen Sie unseren 3-Fragen-Check und finden Sie es heraus',
  button: 'Zum Quick-Check'
},
en: {
  title: 'Which solution is right for me?',
  subtitle: 'Take our 3-question check and find out',
  button: 'Start Quick-Check'
}
```

**User-Journey**:
1. Benutzer scrollt nach Hero
2. Sieht prominente Frage "Welche Lösung passt zu mir?"
3. Klickt auf "Zum Quick-Check"
4. Wird zur Service-Finder-Seite weitergeleitet
5. Macht den 3-Fragen-Check
6. Erhält Service-Empfehlung

---

### Service-Detailseiten

Alle Service-Seiten folgen der gleichen Struktur:

#### 1. DataAnalytics.tsx (`/services/data-analytics`)

**Service**: Datenanalyse & Data Science

**Komponenten**:
- ServiceHero (mit Statistiken)
- QuickCheckButton (6 Fragen)
- OutcomesSection (3 Outcomes)
- ProcessSection (5 Schritte)
- ExamplesSection (3 Beispiele)
- DeliverablesSection (3 Kategorien)
- FAQSection (5 FAQs)
- CTASection
- StickyCTA

**Themen**:
- Datenvisualisierung
- Predictive Analytics
- Machine Learning
- Business Intelligence

---

#### 2. Software.tsx (`/services/softwareentwicklung`)

**Service**: Softwareentwicklung

**Komponenten**:
- ServiceHero
- QuickCheckButton (6 Fragen)
- OutcomesSection (3 Outcomes)
- ProcessSection (5 Schritte)
- ExamplesSection (3 Beispiele)
- DeliverablesSection (3 Kategorien)
- FAQSection (5 FAQs)
- CTASection
- StickyCTA

**Themen**:
- Web-Entwicklung
- Mobile Apps
- API-Entwicklung
- Cloud-Lösungen

---

#### 3. Digitalization.tsx (`/services/digitalisierung`)

**Service**: Digitalisierung

**Komponenten**:
- ServiceHero
- QuickCheckButton (6 Fragen)
- OutcomesSection (3 Outcomes)
- ProcessSection (5 Schritte)
- ExamplesSection (3 Beispiele)
- DeliverablesSection (3 Kategorien)
- FAQSection (5 FAQs)
- CTASection
- StickyCTA

**Themen**:
- Prozessautomatisierung
- Digitale Transformation
- Workflow-Optimierung
- Systemintegration

---

#### 4. Consulting.tsx (`/services/beratung-strategie`)

**Service**: Beratung & Strategie

**Komponenten**:
- ServiceHero
- QuickCheckButton (6 Fragen)
- OutcomesSection (3 Outcomes)
- ProcessSection (5 Schritte)
- ExamplesSection (3 Beispiele)
- DeliverablesSection (3 Kategorien)
- FAQSection (5 FAQs)
- CTASection
- StickyCTA

**Themen**:
- Digital-Strategie
- Change Management
- Technologie-Beratung
- Projektmanagement

---

## Zweisprachigkeit

### Implementierung

**Browser-Sprach-Erkennung**:
```typescript
const getBrowserLanguage = (): 'de' | 'en' => {
  const browserLang = navigator.language.toLowerCase();
  return browserLang.startsWith('de') ? 'de' : 'en';
};
```

**State-Management**:
```typescript
const [language, setLanguage] = useState<'de' | 'en'>(getBrowserLanguage());
```

### Translation-Pattern

Jede Komponente enthält ein `translations`-Objekt:

```typescript
const translations = {
  de: {
    // Deutsche Texte
  },
  en: {
    // Englische Texte
  }
};

const t = translations[language];
```

### Sprachumschalter

**Desktop**:
- Globe-Icon mit Dropdown
- Hover-Aktivierung
- Zeigt: DE / EN

**Mobile**:
- Zwei separate Buttons
- Toggle zwischen Deutsch/English
- Aktive Sprache orange hervorgehoben

---

## Navigation & Routing

### Client-Side-Routing

**Page-State**:
```typescript
type Page = 'home' | 'service-finder' | 'data-analytics' | 'software' | 'digitalization' | 'consulting' | 'admin';
const [currentPage, setCurrentPage] = useState<Page>('home');
```

**Navigation-Funktionen**:

1. **Logo-Click**: Zurück zur Homepage
2. **Service-Click**: Zu Service-Detailseite
3. **Service-Finder-Navigation**: Von Homepage/Service-Seiten zum 3-Fragen-Check
4. **Scroll-to-Section**: Homepage-Sections

**Navigations-Flow**:

```
Homepage
  ↓ (QuickCheckCTA oder Service-Seite Button)
Service-Finder (3-Fragen-Check)
  ↓ (Ergebnis)
Service-Detail-Seite (z.B. Datenanalyse)
  ↓ (CTA oder Kontakt)
Homepage → Kontakt-Section
```

### Service-Navigation

**Von Homepage zur Service-Finder-Seite**:
- QuickCheckCTA-Button (direkt nach Hero)
- QuickCheckButton auf Service-Detailseiten

**Vom Service-Finder zur Service-Detail-Seite**:
- "Mehr erfahren"-Button in der Empfehlungs-Card
- Automatisch nach Beantwortung der 3 Fragen

**Von Homepage zu Service-Seite**:
- "Mehr erfahren"-Button in Services.tsx
- Dropdown-Menü in Navigation

**Von Service-Seite zurück**:
- Logo-Click → Homepage
- Browser-Back-Button

**Kontakt-Navigation**:
- Von überall: Kontakt-Button scrollt zur Homepage-Kontakt-Section
- Cross-Page-Scroll: Navigiert erst zur Homepage, dann scrollt

### Dropdown-Menü

**Desktop**:
- Hover über "Lösungen" öffnet Dropdown
- 4 Service-Optionen
- Nahtloser Übergang ohne Lücke
- `onMouseEnter` / `onMouseLeave`

**Mobile**:
- Click öffnet/schließt Accordion
- Border-left-Design für Sub-Items

---

## Features & Funktionalitäten

### 1. Responsive Design

**Breakpoints** (Tailwind):
- `sm:` 640px
- `md:` 768px
- `lg:` 1024px
- `xl:` 1280px

**Mobile-First-Ansatz**:
- Alle Komponenten mobile-optimiert
- Desktop-Features als Enhancement
- Touch-friendly Buttons und Links

---

### 2. Glassmorphism-Effekte

**Card-Design**:
```css
bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl
```

**Navigation**:
```css
bg-zinc-950/95 backdrop-blur-sm border-b border-zinc-800
```

**Dropdown**:
```css
bg-zinc-900/95 backdrop-blur-sm border border-zinc-800 rounded-xl shadow-2xl shadow-black/50
```

---

### 3. Hover-Animationen

**Text-Links**:
```css
hover:text-[#f7931a] transition-colors
```

**Buttons**:
```css
hover:bg-[#f7931a]/90 transition-all
```

**Cards**:
```css
hover:border-[#f7931a]/50 transition-all
```

**Icons**:
```css
group-hover:scale-110 transition-transform
```

---

### 4. QuickCheck-Interaktivität

**Funktionsweise**:
1. Benutzer klickt "Ja" oder "Nein"
2. Score wird berechnet
3. Dynamische Empfehlung basierend auf Score
4. CTA-Button wird angezeigt

**State-Management**:
```typescript
const [answers, setAnswers] = useState<Record<string, boolean>>({});
const score = Object.values(answers).filter(Boolean).length;
```

---

### 5. FAQ-Accordion

**Funktionsweise**:
1. Click auf Frage öffnet/schließt Antwort
2. ChevronDown rotiert
3. Smooth-Height-Transition
4. Nur eine Antwort gleichzeitig offen (optional)

**State**:
```typescript
const [openIndex, setOpenIndex] = useState<number | null>(null);
```

---

### 6. Kontaktformular

**Validierung**:
- Email-Format
- Pflichtfelder
- Min/Max-Length

**Submit-Flow**:
1. Validierung
2. Mock-API-Call (bereit für Django)
3. Toast-Notification
4. Formular-Reset

**React Hook Form**:
```typescript
const { register, handleSubmit, formState: { errors } } = useForm();
```

---

### 7. Toast-Notifications

**Verwendung**:
```typescript
import { toast } from 'sonner@2.0.3';

// Erfolg
toast.success('Nachricht gesendet!');

// Fehler
toast.error('Ein Fehler ist aufgetreten');
```

**Komponente**:
```tsx
<Toaster position="top-right" />
```

---

### 8. Scroll-Behavior

**Smooth-Scroll**:
```typescript
element.scrollIntoView({ behavior: 'smooth' });
```

**Cross-Page-Navigation**:
```typescript
// Erst zur Homepage navigieren, dann scrollen
if (currentPage !== 'home') {
  onLogoClick();
  setTimeout(() => {
    element.scrollIntoView({ behavior: 'smooth' });
  }, 100);
}
```

---

### 9. Sticky CTA

**Verhalten**:
- Erscheint beim Scrollen
- Fixed Position (bottom)
- Mobile: volle Breite
- Desktop: zentriert mit max-width

**CSS**:
```css
fixed bottom-0 left-0 right-0 z-40 p-4
```

---

## Admin-Panel

### Überblick

Das Admin-Panel ist eine vollständige Verwaltungsoberfläche für die Datalization-Website. Es ermöglicht die einfache Verwaltung von Kontaktanfragen, Case Studies, Kunden und Inhalten ohne Programmierkenntnisse.

**Zugriff**: `/admin` oder durch Eingabe der URL im Browser

**Demo-Login**:
- Benutzername: `admin`
- Passwort: `datalization2026`

---

### Architektur

Das Admin-Panel ist vollständig in React/TypeScript implementiert und nutzt das gleiche Design-System wie die Hauptwebsite:

```
/pages/admin/
├── AdminPanel.tsx           # Haupt-Komponente mit Routing
├── Login.tsx                # Login-Seite mit Mock-Authentifizierung
├── AdminLayout.tsx          # Layout mit Sidebar und Header
├── Dashboard.tsx            # Dashboard mit Übersicht
├── ContactRequests.tsx      # Kontaktanfragen-Verwaltung
├── CaseStudiesManager.tsx   # Case Studies CRUD
├── CustomersManager.tsx     # Kunden-Verwaltung
└── ContentManager.tsx       # Content Management System
```

---

### Features

#### 1. Login-System

**Datei**: `/pages/admin/Login.tsx`

**Features**:
- Mock-Authentifizierung (bereit für echtes Backend)
- Glassmorphism-Design
- Responsive Layout
- Demo-Credentials angezeigt

**Sicherheit** (für Production):
- JWT-Token-basierte Authentifizierung
- Session-Management
- Password-Hashing (bcrypt)
- Rate-Limiting gegen Brute-Force

---

#### 2. Dashboard

**Datei**: `/pages/admin/Dashboard.tsx`

**Features**:
- **Statistiken-Karten**:
  - Kontaktanfragen (Gesamt + neue diese Woche)
  - Case Studies (Gesamt + in Bearbeitung)
  - Kunden (Gesamt + neue diesen Monat)
  - Inhalte (Anzahl + letzte Aktualisierung)

- **Schnellzugriff-Karten**:
  - Direkt zu den Verwaltungs-Bereichen
  - Icon-basierte Navigation
  - Hover-Effekte

- **Letzte Aktivitäten**:
  - Timeline der letzten Änderungen
  - Typen: contact, case, customer, content
  - Zeitstempel

---

#### 3. Kontaktanfragen-Verwaltung

**Datei**: `/pages/admin/ContactRequests.tsx`

**Features**:

**Liste-Ansicht**:
- Alle Kontaktanfragen in Cards
- Status-Badges (Neu, In Bearbeitung, Abgeschlossen, Archiviert)
- Suchfunktion (Name, Email)
- Filter nach Status
- Datum und Service angezeigt

**Detail-Ansicht**:
- Vollständige Kontaktdaten
- Klickbare Email/Telefon-Links
- Nachricht im Volltext
- Service-Auswahl

**Status-Management**:
- 4 Status-Optionen:
  - **Neu** (blau) - Neu eingegangen
  - **In Bearbeitung** (gelb) - Wird bearbeitet
  - **Abgeschlossen** (grün) - Erledigt
  - **Archiviert** (grau) - Archiviert

- Status ändern mit 4 Buttons
- Toast-Notification bei Änderung

**Statistiken**:
- Anzahl pro Status
- Farbcodiert mit Icons

**Aktionen**:
- Status ändern
- Anfrage löschen (mit Bestätigung)

---

#### 4. Case Studies Manager

**Datei**: `/pages/admin/CaseStudiesManager.tsx`

**Features**:

**Liste-Ansicht**:
- Grid-Layout (3 Spalten Desktop)
- Bild-Vorschau
- Titel, Kunde, Beschreibung
- Technologie-Tags (max. 3 + Counter)
- Status-Badge (Veröffentlicht / Entwurf)

**CRUD-Operationen**:

**Create (Neue Case Study)**:
- Modal-Dialog
- Formular mit Feldern:
  - Titel * (required)
  - Kunde * (required)
  - Beschreibung * (required, textarea)
  - Herausforderung (textarea)
  - Lösung (textarea)
  - Ergebnisse (textarea)
  - Technologien (kommagetrennt)
  - Kategorie (Dropdown: Datenanalyse, Softwareentwicklung, Digitalisierung, Beratung)
  - Bild-URL
  - Datum (date-picker)
  - Veröffentlicht (checkbox)

**Read (Anzeigen)**:
- Card-Ansicht mit allen Daten
- Bild-Vorschau

**Update (Bearbeiten)**:
- Gleicher Modal wie Create
- Vorausgefüllte Felder
- "Aktualisieren"-Button

**Delete (Löschen)**:
- Bestätigungs-Dialog
- Toast-Notification

**Veröffentlichen/Verstecken**:
- Toggle-Button
- Ändert Status zwischen veröffentlicht und Entwurf

**Suchfunktion**:
- Suche nach Titel oder Kunde
- Live-Filtering

---

#### 5. Kunden-Verwaltung

**Datei**: `/pages/admin/CustomersManager.tsx`

**Features**:

**Statistiken**:
- Gesamt Kunden
- Aktive Kunden
- Gesamtumsatz (berechnet)

**Tabellen-Ansicht**:
- Vollständige Kundenliste
- Spalten:
  - Kunde (Name + Firma)
  - Kontakt (Email + Telefon mit Icons)
  - Branche
  - Status (Interessent, Aktiv, Inaktiv)
  - Anzahl Projekte
  - Umsatz
  - Aktionen (Bearbeiten, Löschen)

**CRUD-Operationen**:

**Create/Update Modal**:
- Formular mit Feldern:
  - Name * (required)
  - Firma * (required)
  - Email * (required, validated)
  - Telefon
  - Branche
  - Status (Dropdown: Interessent, Aktiv, Inaktiv)
  - Anzahl Projekte (number)
  - Umsatz (text, z.B. "CHF 45'000")
  - Startdatum (date-picker)
  - Notizen (textarea)

**Suchfunktion**:
- Suche nach Name, Firma oder Email
- Live-Filtering

**Status-Badges**:
- Farbcodiert:
  - Interessent (blau)
  - Aktiv (grün)
  - Inaktiv (grau)

---

#### 6. Content Manager

**Datei**: `/pages/admin/ContentManager.tsx`

**Features**:

**Zweisprachiges Editing**:
- Toggle zwischen Deutsch/Englisch
- Beide Sprachen parallel sichtbar
- Live-Vorschau beider Übersetzungen

**Content-Bereiche**:
Organisiert nach Sections:
1. **Hero**
   - Titel
   - Untertitel
   - Beschreibung

2. **Vision**
   - Titel
   - Beschreibung

3. **Services**
   - Section-Titel
   - Section-Beschreibung
   - Service-Titel (alle 4)
   - Service-Beschreibungen (alle 4)

4. **About**
   - Titel
   - Beschreibung

5. **Contact**
   - Titel
   - Beschreibung

6. **Footer**
   - Tagline

**Feld-Typen**:
- **Text-Input**: Für kurze Texte (Titel, etc.)
- **Textarea**: Für längere Texte (Beschreibungen)

**Change-Detection**:
- Ungespeicherte Änderungen werden erkannt
- Warning-Banner oben
- Sticky Save-Bar unten

**Aktionen**:
- **Speichern**: Speichert alle Änderungen
- **Zurücksetzen**: Verwirft alle Änderungen (mit Bestätigung)

**Vergleichs-Ansicht**:
- Beide Sprachen nebeneinander
- Erleichtert Übersetzungs-Konsistenz

---

### Admin-Layout

**Datei**: `/pages/admin/AdminLayout.tsx`

**Komponenten**:

**Top-Bar**:
- Logo + "Admin Panel" Label
- Hamburger-Menu (Mobile)
- Logout-Button

**Sidebar** (Desktop):
- Navigation mit Icons
- 5 Menüpunkte:
  1. Dashboard
  2. Kontaktanfragen
  3. Case Studies
  4. Kunden
  5. Inhalte
- Aktiver Menüpunkt orange hervorgehoben
- Fixed Position

**Mobile-Ansicht**:
- Sidebar als Slide-in von links
- Overlay beim Öffnen
- Auto-Close nach Navigation

---

### State-Management

**Aktuell** (Mock-Daten):
- Lokaler React-State (`useState`)
- Keine Persistenz zwischen Sessions
- Perfekt für Demo und Entwicklung

**Für Production** (Empfohlen):
```typescript
// Option 1: Context API + localStorage
const AdminContext = createContext();

// Option 2: React Query + API
const { data, isLoading } = useQuery('contacts', fetchContacts);

// Option 3: Redux Toolkit
const contacts = useSelector(state => state.contacts);
```

---

### API-Integration (Production)

**Empfohlene Endpunkte**:

```typescript
// Kontaktanfragen
GET    /api/admin/contacts          // Liste
GET    /api/admin/contacts/:id      // Detail
PATCH  /api/admin/contacts/:id      // Status ändern
DELETE /api/admin/contacts/:id      // Löschen

// Case Studies
GET    /api/admin/cases             // Liste
POST   /api/admin/cases             // Erstellen
GET    /api/admin/cases/:id         // Detail
PUT    /api/admin/cases/:id         // Aktualisieren
DELETE /api/admin/cases/:id         // Löschen
PATCH  /api/admin/cases/:id/publish // Veröffentlichen

// Kunden
GET    /api/admin/customers         // Liste
POST   /api/admin/customers         // Erstellen
GET    /api/admin/customers/:id     // Detail
PUT    /api/admin/customers/:id     // Aktualisieren
DELETE /api/admin/customers/:id     // Löschen

// Content
GET    /api/admin/content           // Alle Inhalte
PUT    /api/admin/content           // Batch-Update
```

**Authentifizierung**:
```typescript
// JWT in Header
headers: {
  'Authorization': `Bearer ${token}`
}
```

---

### Sicherheit

**Aktuell** (Demo):
- Mock-Login ohne echte Authentifizierung
- Keine Session-Verwaltung
- Client-seitige Validierung

**Für Production**:

1. **Backend-Authentifizierung**:
   - Django Auth oder JWT
   - Password-Hashing (bcrypt/argon2)
   - Session-Management

2. **Authorization**:
   - Rollensystem (Admin, Editor, Viewer)
   - Permissions pro Bereich
   - Audit-Logging

3. **Input-Validierung**:
   - Backend-Validierung (nie nur Frontend!)
   - XSS-Protection
   - SQL-Injection-Prevention

4. **HTTPS**:
   - Nur über HTTPS erreichbar
   - Secure Cookies

5. **CSRF-Protection**:
   - CSRF-Tokens in Formularen
   - SameSite-Cookies

---

### Berechtigungen (für Production)

**Rollen-Vorschlag**:

| Rolle | Dashboard | Kontakte | Cases | Kunden | Content |
|-------|-----------|----------|-------|--------|---------|
| **Admin** | ✅ | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| **Editor** | ✅ | ✅ Read/Update | ✅ CRUD | ✅ Read/Update | ✅ CRUD |
| **Viewer** | ✅ | ✅ Read | ✅ Read | ✅ Read | ❌ |

---

### Datenbank-Schema (für Production)

**ContactRequest**:
```sql
CREATE TABLE contact_requests (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  service VARCHAR(100),
  message TEXT NOT NULL,
  status ENUM('new', 'in-progress', 'completed', 'archived'),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**CaseStudy**:
```sql
CREATE TABLE case_studies (
  id UUID PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  client VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  challenge TEXT,
  solution TEXT,
  results TEXT,
  technologies TEXT[], -- Array of strings
  category VARCHAR(100),
  image_url VARCHAR(500),
  date DATE,
  published BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Customer**:
```sql
CREATE TABLE customers (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  company VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  industry VARCHAR(100),
  status ENUM('prospect', 'active', 'inactive'),
  projects_count INTEGER DEFAULT 0,
  revenue VARCHAR(50),
  start_date DATE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Content**:
```sql
CREATE TABLE content (
  id UUID PRIMARY KEY,
  section VARCHAR(100) NOT NULL,
  key VARCHAR(255) NOT NULL,
  value_de TEXT NOT NULL,
  value_en TEXT NOT NULL,
  type ENUM('text', 'textarea'),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(section, key)
);
```

---

### Verwendung

**1. Admin-Panel aufrufen**:
```
http://localhost:5173/admin
```

**2. Login**:
- Benutzername: `admin`
- Passwort: `datalization2026`

**3. Navigation**:
- Dashboard für Übersicht
- Sidebar für Bereiche
- Mobile: Hamburger-Menu

**4. Kontaktanfragen verwalten**:
- Liste durchsuchen
- Anfrage auswählen
- Status ändern
- Bei Bedarf löschen

**5. Case Studies erstellen**:
- "Neue Case Study" Button
- Formular ausfüllen
- Speichern oder veröffentlichen

**6. Kunden hinzufügen**:
- "Neuer Kunde" Button
- Kundendaten eingeben
- Status festlegen
- Speichern

**7. Inhalte bearbeiten**:
- Section auswählen
- Sprache wählen (DE/EN)
- Text bearbeiten
- Speichern

---

### Styling & Design

**Konsistent mit Hauptwebsite**:
- Zinc-950 Hintergrund
- Orange (#f7931a) Akzente
- Glassmorphism-Effekte
- Gleiche Buttons und Inputs
- Responsive Design

**Admin-spezifische Elemente**:
- Sidebar-Navigation
- Tabellen-Layouts
- Modal-Dialoge
- Status-Badges
- Toast-Notifications

---

### Performance

**Optimierungen**:
- Lazy-Loading von Komponenten
- Virtualisierte Listen (für große Datenmengen)
- Debounced-Search
- Pagination (für Production)

**Empfohlen für Production**:
```typescript
// Lazy Loading
const ContactRequests = lazy(() => import('./ContactRequests'));

// Virtualized List (react-window)
import { FixedSizeList } from 'react-window';

// Debounced Search
import { useDebouncedValue } from '@/hooks/useDebouncedValue';
```

---

### Testing

**Empfohlene Tests**:

**1. Login-Tests**:
- Erfolgreicher Login
- Fehlgeschlagener Login
- Logout

**2. CRUD-Tests**:
- Erstellen von Einträgen
- Bearbeiten von Einträgen
- Löschen von Einträgen
- Validierung

**3. Status-Tests**:
- Status-Änderungen
- Filter-Funktionen
- Suchfunktionen

**4. Content-Tests**:
- Zweisprachiges Editing
- Speichern/Zurücksetzen
- Change-Detection

---

### Erweiterungen

**Mögliche zusätzliche Features**:

1. **Statistiken & Analytics**:
   - Diagramme (Recharts)
   - Conversion-Rates
   - Service-Popularität

2. **Email-Integration**:
   - Email-Benachrichtigungen
   - Direkt aus Admin antworten
   - Email-Templates

3. **Export-Funktionen**:
   - CSV-Export
   - PDF-Reports
   - Excel-Downloads

4. **Medien-Bibliothek**:
   - Bild-Upload
   - Medien-Verwaltung
   - Image-Resizing

5. **Versionierung**:
   - Content-History
   - Rollback-Funktion
   - Audit-Trail

6. **Multi-Benutzer**:
   - Benutzer-Verwaltung
   - Rollen & Permissions
   - Team-Kollaboration

7. **Backup & Restore**:
   - Automatische Backups
   - Restore-Funktion
   - Export/Import

---

### Migration zu Production

**Schritte**:

1. **Backend aufsetzen** (Django/Node.js):
   ```bash
   # Django
   django-admin startproject datalization_admin
   
   # Node.js + Express
   npm init
   npm install express prisma @prisma/client
   ```

2. **Datenbank erstellen**:
   - PostgreSQL empfohlen
   - Migrations anlegen
   - Seed-Daten einfügen

3. **API-Endpunkte implementieren**:
   - RESTful API
   - Authentifizierung
   - Validierung

4. **Frontend anpassen**:
   - Mock-Daten durch API-Calls ersetzen
   - Error-Handling
   - Loading-States

5. **Deployment**:
   - Frontend: Vercel/Netlify
   - Backend: Railway/Render
   - Datenbank: Supabase/PlanetScale

---

## Deployment & Integration

### Vite-Build

**Entwicklung**:
```bash
npm run dev
```

**Production-Build**:
```bash
npm run build
```

Output: `/dist`-Ordner

---

### Django-Integration

**Vorbereitung**:
1. ✅ Alle Komponenten sind statisch
2. ✅ Kein komplexes State-Management
3. ✅ Props-basierte Architektur
4. ✅ Zweisprachigkeit vorbereitet

**Integration-Schritte**:

1. **Static Files**:
   - Build-Output in Django-Static-Folder
   - `STATIC_URL` und `STATICFILES_DIRS` konfigurieren

2. **Templates**:
   - Komponenten in Django-Templates konvertieren
   - `{% load static %}` für Assets

3. **Backend-Logik**:
   - Kontaktformular: Django-View erstellen
   - Service-Data: Aus Django-Models laden
   - Case Studies: Database-driven

4. **Mehrsprachigkeit**:
   - Django i18n verwenden
   - `{% trans %}` und `{% blocktrans %}`
   - `LANGUAGE_CODE` und `LANGUAGES` in settings.py

5. **Routing**:
   - URL-Patterns in `urls.py` definieren
   - View-Functions oder Class-Based-Views

---

### Environment Variables

**Für API-Keys** (falls benötigt):
```env
VITE_API_URL=https://api.example.com
VITE_CONTACT_EMAIL=info@datalization.ch
```

**Zugriff in Code**:
```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```

---

### Performance-Optimierung

**Empfehlungen**:

1. **Code-Splitting**:
   - Lazy-Loading für Service-Pages
   ```typescript
   const DataAnalytics = lazy(() => import('./pages/services/DataAnalytics'));
   ```

2. **Image-Optimierung**:
   - WebP-Format verwenden
   - Lazy-Loading: `loading="lazy"`
   - Responsive Images: `srcset`

3. **CSS-Optimierung**:
   - Tailwind-Purge aktiviert (automatisch in Production)
   - Minimal Custom-CSS

4. **Bundle-Größe**:
   - Tree-Shaking aktiviert
   - Nur benötigte Icon-Imports

---

### SEO-Optimierung

**Empfehlungen**:

1. **Meta-Tags** (index.html):
   ```html
   <meta name="description" content="Datalization - Datenanalyse und Digitalisierung">
   <meta name="keywords" content="Datenanalyse, Data Science, Digitalisierung">
   ```

2. **Semantic HTML**:
   - Korrekte Heading-Hierarchie (h1 > h2 > h3)
   - `<nav>`, `<main>`, `<footer>`, `<section>`

3. **Alt-Texte**:
   - Für alle Bilder und Icons

4. **Structured Data** (optional):
   - JSON-LD für Organization
   - Service-Schema

---

### Accessibility (A11y)

**Implementiert**:

1. **Keyboard-Navigation**:
   - Alle interaktiven Elemente erreichbar
   - Focus-Styles vorhanden

2. **ARIA-Labels**:
   - Buttons mit aussagekräftigen Labels
   - `aria-expanded` für Dropdowns

3. **Kontrast**:
   - Weiß auf Dunkel (hoher Kontrast)
   - Orange-Akzente gut sichtbar

4. **Screen-Reader**:
   - Semantische HTML-Struktur
   - Alt-Texte für Bilder

---

### Testing

**Empfohlene Tests**:

1. **Unit-Tests** (Jest + React Testing Library):
   - Komponenten-Rendering
   - Props-Handling
   - User-Interaktionen

2. **Integration-Tests**:
   - Navigation-Flow
   - Formular-Submit
   - Sprachumschaltung

3. **E2E-Tests** (Playwright/Cypress):
   - User-Journeys
   - Service-Navigation
   - Kontaktformular-Submit

---

### Browser-Kompatibilität

**Unterstützte Browser**:
- Chrome/Edge (letzte 2 Versionen)
- Firefox (letzte 2 Versionen)
- Safari (letzte 2 Versionen)

**Polyfills** (falls benötigt):
- CSS `backdrop-filter` (ältere Browser)

---

### Wartung & Updates

**Regelmäßige Aufgaben**:

1. **Dependency-Updates**:
   ```bash
   npm outdated
   npm update
   ```

2. **Security-Audit**:
   ```bash
   npm audit
   npm audit fix
   ```

3. **Content-Updates**:
   - Case Studies aktualisieren
   - Service-Beschreibungen anpassen
   - FAQs erweitern

---

### Erweiterungsmöglichkeiten

**Potenzielle Features**:

1. **Blog-Section**:
   - Artikel zu Themen
   - Kategorisierung
   - Suchfunktion

2. **Projekt-Portfolio**:
   - Detaillierte Case-Study-Pages
   - Projekt-Filter
   - Technologie-Tags

3. **Team-Seite**:
   - Mitarbeiter-Profile
   - Expertise-Bereiche
   - Kontaktmöglichkeiten

4. **Ressourcen**:
   - Downloads (Whitepapers, etc.)
   - Tools & Rechner
   - Glossar

5. **Karriere**:
   - Job-Angebote
   - Bewerbungsformular

6. **Customer-Portal** (Django):
   - Login-System
   - Projekt-Dashboard
   - Dokumenten-Upload

---

## Zusammenfassung

### Stärken der Implementierung

✅ **Vollständig zweisprachig** (DE/EN) mit Browser-Erkennung  
✅ **4 Service-Detailseiten** mit je 8 wiederverwendbaren Komponenten  
✅ **Responsive Design** (Mobile-First)  
✅ **Moderne UI** (Glassmorphism, Hover-Animationen)  
✅ **Interaktive Elemente** (QuickCheck, FAQ-Accordion)  
✅ **Funktionierendes Kontaktformular** mit Validierung  
✅ **Django-ready** Architektur  
✅ **Konsistentes Design-System** (Orange-Akzente, Zinc-Grautöne)  
✅ **Performant** (Vite, minimales JavaScript)  
✅ **Wartbar** (Modulare Komponenten, klare Struktur)  

### Wichtige Dateien

| Datei | Beschreibung |
|-------|--------------|
| `/App.tsx` | Haupt-App mit Routing |
| `/components/Navigation.tsx` | Navigation mit Dropdown & Sprachumschalter |
| `/components/Contact.tsx` | Kontaktformular |
| `/components/service-details/*.tsx` | 8 Service-Detail-Komponenten |
| `/pages/services/*.tsx` | 4 Service-Detailseiten |
| `/styles/globals.css` | Design-System & Tailwind-Config |

---

**Letzte Aktualisierung**: Januar 2026  
**Version**: 2.0  
**Autor**: Datalization Team  
**Kontakt**: info@datalization.ch