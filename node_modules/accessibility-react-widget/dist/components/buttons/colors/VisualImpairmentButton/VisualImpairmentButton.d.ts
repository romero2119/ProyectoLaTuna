import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface VisualImpairmentButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const VisualImpairmentButton: FC<VisualImpairmentButtonProps>;
export default VisualImpairmentButton;
