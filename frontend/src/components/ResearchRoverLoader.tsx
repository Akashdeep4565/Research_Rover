import { motion } from 'framer-motion'

export interface ResearchRoverLoaderProps {
  message?: string
  fullscreen?: boolean
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function ResearchRoverLoader({
  message = 'Research ROVER is loading...',
  fullscreen = false,
  size = 'md',
  className = '',
}: ResearchRoverLoaderProps) {
  // Dimension mappings
  const sizeConfig = {
    sm: {
      logoWidth: 'w-20',
      dots: 'w-1.5 h-1.5',
      text: 'text-xs font-medium',
      gap: 'space-y-3',
    },
    md: {
      logoWidth: 'w-32',
      dots: 'w-2 h-2',
      text: 'text-sm font-medium',
      gap: 'space-y-4',
    },
    lg: {
      logoWidth: 'w-44',
      dots: 'w-2.5 h-2.5',
      text: 'text-base font-semibold',
      gap: 'space-y-5',
    },
  }[size]

  const loaderContent = (
    <div className={`flex flex-col items-center justify-center text-center select-none ${sizeConfig.gap} ${className}`}>
      {/* Central Logo with subtle pulse & scale */}
      <motion.div
        animate={{
          opacity: [0.85, 1, 0.85],
          scale: [0.98, 1.02, 0.98],
        }}
        transition={{
          repeat: Infinity,
          duration: 2.2,
          ease: 'easeInOut',
        }}
        className="relative flex items-center justify-center"
      >
        <img
          src="/assets/research-rover-logo.png"
          alt="Research ROVER"
          className={`${sizeConfig.logoWidth} h-auto object-contain drop-shadow-sm`}
        />
      </motion.div>

      {/* Subtle 3-dot loading indicator */}
      <div className="flex items-center space-x-2 my-1">
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            className={`${sizeConfig.dots} rounded-full bg-blue-600 dark:bg-blue-400`}
            animate={{
              scale: [0.75, 1.25, 0.75],
              opacity: [0.35, 1, 0.35],
            }}
            transition={{
              repeat: Infinity,
              duration: 1.2,
              delay: i * 0.2,
              ease: 'easeInOut',
            }}
          />
        ))}
      </div>

      {/* Message */}
      {message && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className={`${sizeConfig.text} text-slate-600 dark:text-slate-300 tracking-wide`}
        >
          {message}
        </motion.p>
      )}
    </div>
  )

  if (fullscreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/85 dark:bg-slate-900/85 backdrop-blur-md transition-all duration-300">
        {loaderContent}
      </div>
    )
  }

  return loaderContent
}
