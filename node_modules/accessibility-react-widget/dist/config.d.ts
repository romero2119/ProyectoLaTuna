import { IconSvgComponent } from './types';

export declare const langOptions: {
    label: string;
    value: string;
}[];
export declare const langMap: Record<string, {
    label: string;
    value: string;
}>;
type Collapsed = {
    name: string;
    isExpanded: boolean;
    icon: IconSvgComponent;
};
export interface CollapsedState {
    content: Collapsed;
    colors: Collapsed;
    tools: Collapsed;
}
export declare const collapsedStateInit: CollapsedState;
export type CollapsedStateKeys = keyof typeof collapsedStateInit;
export {};
