import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface LetterSpacingButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const LetterSpacingButton: FC<LetterSpacingButtonProps>;
export default LetterSpacingButton;
