import { FC } from 'react';

interface RcSliderProps {
    range?: boolean;
    min?: number;
    max?: number;
    value?: number;
    onChange: (n: number | number[]) => void;
    height?: number;
    vertical?: boolean;
}
declare const RcSlider: FC<RcSliderProps>;
export default RcSlider;
