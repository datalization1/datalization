import { motion, AnimatePresence } from 'motion/react';
import { useState, useEffect } from 'react';
import { Calendar, X } from 'lucide-react';

interface StickyCTAProps {
  text: string;
  onClick: () => void;
}

export function StickyCTA({ text, onClick }: StickyCTAProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isDismissed, setIsDismissed] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      // Show CTA after scrolling 500px
      if (window.scrollY > 500 && !isDismissed) {
        setIsVisible(true);
      } else if (window.scrollY <= 500) {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isDismissed]);

  const handleDismiss = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsDismissed(true);
    setIsVisible(false);
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          className="fixed bottom-8 right-8 z-50"
        >
          <div className="relative group">
            {/* Dismiss Button */}
            <button
              onClick={handleDismiss}
              className="absolute -top-2 -right-2 w-6 h-6 bg-zinc-800 hover:bg-zinc-700 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity z-10"
              aria-label="Dismiss"
            >
              <X className="w-4 h-4" />
            </button>

            {/* CTA Button */}
            <button
              onClick={onClick}
              className="flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-[#f7931a] to-[#f7931a]/80 text-zinc-950 rounded-full shadow-lg shadow-[#f7931a]/30 hover:shadow-xl hover:shadow-[#f7931a]/40 transition-all duration-300 hover:scale-105 font-medium"
            >
              <Calendar className="w-5 h-5" />
              <span>{text}</span>
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}