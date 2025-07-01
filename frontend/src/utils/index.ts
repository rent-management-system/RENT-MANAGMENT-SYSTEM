// Utility function for className merging (tailwind, etc)
export function cn(...args: any[]): string {
  return args.filter(Boolean).join(' ');
}
