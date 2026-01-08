import { useState } from 'react';
import { Lock, User } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { toast } from 'sonner@2.0.3';
import logo from 'figma:asset/9c79fd0c49d5bb3ae17428ccf646e5ea86915053.png';

interface LoginProps {
  onLogin: () => void;
}

export function Login({ onLogin }: LoginProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Mock authentication - in production, this would be a real API call
    setTimeout(() => {
      if (username === 'admin' && password === 'datalization2026') {
        toast.success('Erfolgreich eingeloggt!');
        onLogin();
      } else {
        toast.error('Ungültige Anmeldedaten');
      }
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <img src={logo} alt="Datalization" className="w-16 h-16" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Admin Login</h1>
          <p className="text-zinc-400">Melden Sie sich an, um fortzufahren</p>
        </div>

        <div className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-xl p-8">
          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-2">
                Benutzername
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#f7931a]/50"
                  placeholder="admin"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-2">
                Passwort
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-[#f7931a]/50"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-[#f7931a] hover:bg-[#f7931a]/90 text-white py-3"
              disabled={loading}
            >
              {loading ? 'Wird angemeldet...' : 'Anmelden'}
            </Button>
          </form>

          <div className="mt-6 p-4 bg-zinc-800/30 border border-zinc-700 rounded-lg">
            <p className="text-xs text-zinc-400 text-center">
              Demo-Zugang: <span className="text-[#f7931a]">admin</span> / <span className="text-[#f7931a]">datalization2026</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
