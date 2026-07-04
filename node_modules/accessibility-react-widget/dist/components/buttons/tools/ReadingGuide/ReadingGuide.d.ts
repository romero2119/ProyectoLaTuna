import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface ReadingGuideProps {
    rgGap?: number;
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const ReadingGuide: FC<ReadingGuideProps>;
export default ReadingGuide;
