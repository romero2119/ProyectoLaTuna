import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface HighlightTitlesButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const HighlightTitlesButton: FC<HighlightTitlesButtonProps>;
export default HighlightTitlesButton;
