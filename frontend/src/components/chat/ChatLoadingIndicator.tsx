import { motion } from 'framer-motion'
import { CpuChipIcon, StopIcon } from '@heroicons/react/24/outline'

interface ChatLoadingIndicatorProps {
  onStop?: () => void
  statusMessage?: string
}

export function ChatLoadingIndicator({
  onStop,
  statusMessage = 'Research Rover is searching indexed papers and generating response…',
}: ChatLoadingIndicatorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="flex items-start gap-3.5 my-2"
    >
      {/* Avatar */}
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-sky-400/40 bg-sky-500/10 text-sky-500 shadow-sm dark:border-sky-500/30 dark:bg-sky-950/40 dark:text-sky-400">
        <CpuChipIcon className="h-5 w-5 animate-pulse" />
      </div>

      {/* Bubble card */}
      <div className="flex flex-col gap-2 rounded-2xl border border-gray-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-4 shadow-sm backdrop-blur-sm max-w-xl">
        <div className="flex items-center gap-3">
          {/* Animated typing dots */}
          <div className="flex items-center gap-1.5 px-1">
            <span className="h-2.5 w-2.5 rounded-full bg-sky-500 animate-bounce [animation-delay:-0.3s]" />
            <span className="h-2.5 w-2.5 rounded-full bg-indigo-500 animate-bounce [animation-delay:-0.15s]" />
            <span className="h-2.5 w-2.5 rounded-full bg-sky-400 animate-bounce" />
          </div>
          <span className="text-xs font-semibold text-gray-700 dark:text-slate-300">
            {statusMessage}
          </span>
        </div>

        {onStop && (
          <div className="pt-1 flex items-center justify-between border-t border-gray-100 dark:border-slate-800/80">
            <span className="text-[11px] text-gray-400 dark:text-slate-500">
              Analysis in progress
            </span>
            <button
              type="button"
              onClick={onStop}
              className="flex items-center gap-1.5 rounded-lg border border-rose-200 dark:border-rose-900/60 bg-rose-50/70 dark:bg-rose-950/40 px-2.5 py-1 text-xs font-medium text-rose-600 dark:text-rose-400 hover:bg-rose-100 dark:hover:bg-rose-900/60 transition shadow-sm"
            >
              <StopIcon className="h-3.5 w-3.5 stroke-[2.5]" />
              <span>Stop Generating</span>
            </button>
          </div>
        )}
      </div>
    </motion.div>
  )
}
