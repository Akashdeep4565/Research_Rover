import { Link } from 'react-router-dom'
import { useSystemStatus } from '@/context/SystemStatusContext'

export function Footer() {
  const { apiStatus, modelStatus } = useSystemStatus()

  return (
    <footer className="mt-16 bg-surface-container-lowest/70 dark:bg-slate-900/70 backdrop-blur-md border-t border-outline-variant/30 text-on-surface-variant transition-colors duration-200">
      <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand & Description */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-3 mb-3">
              <img
                src="/assets/research-rover-logo.png"
                alt="Research ROVER"
                className="h-7 w-auto object-contain"
              />
              <span className="font-display font-bold text-lg text-on-surface tracking-tight">
                Research Rover
              </span>
              <span className="px-2 py-0.5 rounded-full bg-primary-fixed text-primary dark:bg-primary-container dark:text-white text-[10px] font-mono font-semibold uppercase">
                v2.4
              </span>
            </div>
            <p className="text-on-surface-variant text-sm max-w-md leading-relaxed mb-4">
              Next-generation scholarly discovery and multi-modal literature analysis platform.
              Synthesize scientific literature with generative research intelligence.
            </p>
            {/* Live System Telemetry Chip (Real Data) */}
            <div className="inline-flex items-center gap-3 px-3 py-1.5 rounded-full bg-surface-container-low/80 dark:bg-slate-800/60 border border-outline-variant/30 text-xs font-mono">
              <div className="flex items-center gap-1.5">
                <span
                  className={`w-2 h-2 rounded-full ${
                    apiStatus === 'online'
                      ? 'bg-emerald-500'
                      : apiStatus === 'offline'
                      ? 'bg-rose-500'
                      : 'bg-amber-500 animate-pulse'
                  }`}
                />
                <span className="text-on-surface">API: {apiStatus}</span>
              </div>
              <span className="text-outline-variant">•</span>
              <div className="flex items-center gap-1.5">
                <span
                  className={`w-2 h-2 rounded-full ${
                    modelStatus === 'loaded'
                      ? 'bg-emerald-500'
                      : modelStatus === 'loading' || modelStatus === 'partial'
                      ? 'bg-amber-500 animate-pulse'
                      : 'bg-rose-500'
                  }`}
                />
                <span className="text-on-surface">Models: {modelStatus}</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-display font-semibold text-xs text-on-surface uppercase tracking-wider mb-4 font-mono">
              Research Workspace
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link 
                  to="/search" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  Search Papers
                </Link>
              </li>
              <li>
                <Link 
                  to="/chat" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  AI Co-Scientist
                </Link>
              </li>
              <li>
                <Link 
                  to="/analytics" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  Meta-Analytics
                </Link>
              </li>
              <li>
                <Link 
                  to="/settings" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  Lab Settings
                </Link>
              </li>
            </ul>
          </div>

          {/* Support & Docs */}
          <div>
            <h3 className="font-display font-semibold text-xs text-on-surface uppercase tracking-wider mb-4 font-mono">
              Documentation
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a 
                  href="#" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  API Reference
                </a>
              </li>
              <li>
                <a 
                  href="#" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  Documentation
                </a>
              </li>
              <li>
                <Link 
                  to="/use-cases" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  Use Cases & Guides
                </Link>
              </li>
              <li>
                <a 
                  href="#" 
                  className="text-on-surface-variant hover:text-primary transition-colors"
                >
                  Report Issue
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Legal & Copyright Bar */}
        <div className="mt-8 pt-6 border-t border-outline-variant/30 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-on-surface-variant">
          <p>© 2026 Research Rover. Built for biomedical & multi-disciplinary scholars.</p>
          <div className="flex items-center space-x-6">
            <a 
              href="#" 
              className="text-on-surface-variant hover:text-on-surface transition-colors"
            >
              Privacy Policy
            </a>
            <a 
              href="#" 
              className="text-on-surface-variant hover:text-on-surface transition-colors"
            >
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
