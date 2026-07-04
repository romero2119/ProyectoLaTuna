import { FC } from 'react';

interface AccValueControlProps {
    onIncrease: () => void;
    onToggle: () => void;
    onDescrease: () => void;
}
declare const AccValueControl: FC<AccValueControlProps>;
export default AccValueControl;
