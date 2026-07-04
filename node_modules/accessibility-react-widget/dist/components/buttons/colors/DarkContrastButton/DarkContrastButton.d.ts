import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface DarkContrastButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const DarkContrastButton: FC<DarkContrastButtonProps>;
export default DarkContrastButton;
