import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface ZoomButtonProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const ZoomButton: FC<ZoomButtonProps>;
export default ZoomButton;
