import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../types';

interface AccColorsProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const AccColors: FC<AccColorsProps>;
export default AccColors;
