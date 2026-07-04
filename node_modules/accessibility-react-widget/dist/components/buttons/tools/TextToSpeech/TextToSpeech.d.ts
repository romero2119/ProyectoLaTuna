import { FC } from 'react';
import { AccessibilikState, ChangeAccDraftHander } from '../../../../types';

interface TextToSpeechProps {
    accState: AccessibilikState;
    onChangeAccState: (fn: ChangeAccDraftHander) => void;
}
declare const TextToSpeech: FC<TextToSpeechProps>;
export default TextToSpeech;
