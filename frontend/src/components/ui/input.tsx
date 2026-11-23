import * as React from "react"

import { cn } from "@/lib/utils"

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-xl border border-outline-variant/50 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-sm px-4 py-2 text-sm text-on-surface shadow-inner-sm transition-all duration-200 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-on-surface placeholder:text-on-surface-variant/60 focus-visible:outline-none focus-visible:border-primary focus-visible:ring-4 focus-visible:ring-primary/10 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
