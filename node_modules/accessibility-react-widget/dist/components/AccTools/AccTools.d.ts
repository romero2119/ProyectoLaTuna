import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../types';

interface AccToolsProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const AccTools: FC<AccToolsProps>;
export default AccTools;
