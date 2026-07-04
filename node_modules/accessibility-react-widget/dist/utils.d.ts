import { AccessibilikState } from './types';

export declare const isRuleAppliedToElement: (element: HTMLElement, rule: CSSStyleRule) => boolean;
export declare const getComputedStyleAndSetAccDataFontSize: (elem: HTMLElement) => void;
export declare const getDataImageSvgBase64: (svg: string) => string;
export declare const getAccInitState: () => AccessibilikState;
export declare const registerDomain: () => Promise<void>;
