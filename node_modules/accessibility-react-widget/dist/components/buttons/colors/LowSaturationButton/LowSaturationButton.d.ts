import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface LowSaturationButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const LowSaturationButton: FC<LowSaturationButtonProps>;
export default LowSaturationButton;
