import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../components/utils";

const badgeVariants = cva(
  "px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider",
  {
    variants: {
      variant: {
        low: "bg-green-100 text-green-700",
        medium: "bg-orange-100 text-orange-700",
        high: "bg-red-100 text-red-700",
        critical: "bg-red-600 text-white",
        pii: "bg-pink-600 text-white",
        persistent: "bg-orange-50 text-orange-600 border border-orange-200",
        info: "bg-slate-100 text-slate-600",
      },
    },
    defaultVariants: {
      variant: "info",
    },
  }
);

export function RiskBadge({ className, variant, ...props }: React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof badgeVariants>) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}