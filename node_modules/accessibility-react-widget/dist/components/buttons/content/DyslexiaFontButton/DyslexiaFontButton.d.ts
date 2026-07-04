import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface DyslexiaFontButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const DyslexiaFontButton: FC<DyslexiaFontButtonProps>;
export default DyslexiaFontButton;
