import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold tracking-wide transition-colors focus:outline-none focus:ring-2 focus:ring-primary/40 focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary-fixed text-primary dark:bg-primary-container dark:text-white shadow-sm",
        secondary:
          "border-transparent bg-secondary-container/40 text-on-secondary-container dark:bg-secondary-container/30 dark:text-teal-200",
        destructive:
          "border-transparent bg-tertiary-container/20 text-tertiary dark:bg-tertiary-container dark:text-white shadow-sm",
        outline: "border-outline-variant/60 text-on-surface-variant bg-transparent",
        primary: "border-transparent bg-primary text-white shadow-sm",
        tertiary: "border-transparent bg-tertiary-container/30 text-tertiary dark:text-rose-200",
        success: "border-transparent bg-emerald-100 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300",
        code: "font-mono text-[11px] rounded-full border border-outline-variant/40 bg-surface-container-low text-on-surface-variant px-2 py-0.5",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
