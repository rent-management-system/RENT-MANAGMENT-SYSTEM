import * as React from "react";
import * as SelectPrimitive from "@radix-ui/react-select";
import { type VariantProps } from "class-variance-authority";

declare const Select: React.FC<SelectPrimitive.SelectProps>;
declare const SelectGroup: React.FC<SelectPrimitive.SelectGroupProps>;
declare const SelectValue: React.FC<SelectPrimitive.SelectValueProps>;
declare const SelectTrigger: React.ForwardRefExoticComponent<SelectPrimitive.SelectTriggerProps & React.RefAttributes<HTMLButtonElement>>;
declare const SelectContent: React.ForwardRefExoticComponent<SelectPrimitive.SelectContentProps & React.RefAttributes<HTMLDivElement>>;
declare const SelectLabel: React.ForwardRefExoticComponent<SelectPrimitive.SelectLabelProps & React.RefAttributes<HTMLDivElement>>;
declare const SelectItem: React.ForwardRefExoticComponent<SelectPrimitive.SelectItemProps & React.RefAttributes<HTMLDivElement>>;
declare const SelectSeparator: React.ForwardRefExoticComponent<SelectPrimitive.SelectSeparatorProps & React.RefAttributes<HTMLDivElement>>;

export { Select, SelectGroup, SelectValue, SelectTrigger, SelectContent, SelectLabel, SelectItem, SelectSeparator };
