import { jsx as _jsx } from "react/jsx-runtime";
import { useTheme } from "next-themes";
import { Toaster } from "sonner";
const SonnerToaster = ({ ...props }) => {
    const { theme = "system" } = useTheme();
    return (_jsx(Toaster, { theme: theme, className: "toaster group", style: {
            "--normal-bg": "var(--popover)",
            "--normal-text": "var(--popover-foreground)",
            "--normal-border": "var(--border)",
        }, ...props }));
};
export { SonnerToaster as Sonner };
