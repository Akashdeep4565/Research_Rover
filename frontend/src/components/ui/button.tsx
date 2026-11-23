import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:ring-offset-1 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 active:scale-[0.98]",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-white shadow-sm shadow-primary/25 hover:bg-primary/90 hover:shadow-md hover:shadow-primary/30",
        destructive:
          "bg-tertiary text-white shadow-sm shadow-tertiary/20 hover:bg-tertiary/90 hover:shadow-md hover:shadow-tertiary/25",
        outline:
          "border border-outline-variant/60 bg-surface-container-lowest/80 text-on-surface hover:bg-surface-container-low hover:border-outline-variant hover:text-on-surface shadow-sm",
        secondary:
          "bg-secondary text-white shadow-sm shadow-secondary/25 hover:bg-secondary/90 hover:shadow-md hover:shadow-secondary/30",
        ghost: "hover:bg-surface-container-high/60 text-on-surface hover:text-on-surface",
        link: "text-primary underline-offset-4 hover:underline",
        glass:
          "bg-surface-container-lowest/80 dark:bg-slate-900/80 backdrop-blur-md border border-white/60 dark:border-white/10 text-on-surface hover:bg-surface-container-lowest shadow-sm hover:shadow-md",
        accent:
          "bg-primary-container text-white shadow-sm shadow-primary-container/25 hover:bg-primary-container/90 hover:shadow-md",
      },
      size: {
        default: "h-9 rounded-full px-4 py-2 font-medium",
        sm: "h-8 rounded-full px-3 text-xs font-medium",
        lg: "h-11 rounded-full px-7 text-base font-semibold",
        icon: "h-9 w-9 rounded-full",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
