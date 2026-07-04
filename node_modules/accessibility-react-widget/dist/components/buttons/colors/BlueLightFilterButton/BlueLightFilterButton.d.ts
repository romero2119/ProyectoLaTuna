import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface BlueLightFilterButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const BlueLightFilterButton: FC<BlueLightFilterButtonProps>;
export default BlueLightFilterButton;
