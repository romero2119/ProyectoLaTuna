import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface WordSpacingButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const WordSpacingButton: FC<WordSpacingButtonProps>;
export default WordSpacingButton;
