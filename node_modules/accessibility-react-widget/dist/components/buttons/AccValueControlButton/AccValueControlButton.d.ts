import { CSSProperties, FC } from 'react';

export type ValueControlType = "init" | "increase" | "decrease";
interface AccValueControlButtonProps {
    controlType: ValueControlType;
    onClick?: () => void;
    style?: CSSProperties;
}
declare const AccValueControlButton: FC<AccValueControlButtonProps>;
export default AccValueControlButton;
