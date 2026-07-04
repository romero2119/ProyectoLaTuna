import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface HighlightLinksButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const HighlightLinksButton: FC<HighlightLinksButtonProps>;
export default HighlightLinksButton;
