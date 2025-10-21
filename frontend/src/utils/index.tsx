// Utility function for className merging (tailwind, etc)
export function cn(...args) {
  return args.filter(Boolean).join(' ');
}
