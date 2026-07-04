import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface TextColorPickerButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const TextColorPickerButton: FC<TextColorPickerButtonProps>;
export default TextColorPickerButton;
