import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface HighSaturationButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const HighSaturationButton: FC<HighSaturationButtonProps>;
export default HighSaturationButton;
