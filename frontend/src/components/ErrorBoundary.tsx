import { Component, type ErrorInfo, type ReactNode } from 'react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface Props {
  children: ReactNode
  fallbackTitle?: string
  fallbackMessage?: string
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  public override state: State = {
    hasError: false,
    error: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public override componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[ErrorBoundary caught error]:', error, errorInfo)
  }

  public override render() {
    if (this.state.hasError) {
      return (
        <div className="rounded-2xl border border-amber-500/30 bg-amber-500/5 p-6 text-center shadow-sm">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/10 text-amber-500">
            <ExclamationTriangleIcon className="h-6 w-6" />
          </div>
          <h4 className="text-sm font-bold text-gray-900 dark:text-slate-100">
            {this.props.fallbackTitle || 'Component Unavailable'}
          </h4>
          <p className="mt-1 text-xs text-gray-500 dark:text-slate-400">
            {this.props.fallbackMessage || 'This section could not be loaded due to a rendering issue.'}
          </p>
          {this.state.error?.message && (
            <p className="mt-2 text-[11px] font-mono text-amber-600 dark:text-amber-400">
              {this.state.error.message}
            </p>
          )}
        </div>
      )
    }

    return this.props.children
  }
}
