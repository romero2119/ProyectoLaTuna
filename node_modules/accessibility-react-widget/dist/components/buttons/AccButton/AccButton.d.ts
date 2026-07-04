import { FC, ReactNode } from 'react';
import { IconSvgComponent } from '../../../types';

interface AccButtonProps {
    Icon: IconSvgComponent;
    isToggled?: boolean;
    isActive?: boolean;
    children?: ReactNode;
    onToggle?: () => void;
    titleTranslationKey: string;
    elementType?: string;
    title?: string;
    stats?: number | string;
    styleIcon?: {
        [x: string]: unknown;
    };
    styleTitle?: {
        [x: string]: unknown;
    };
    className?: string;
    tooltipTranslationKey?: string;
}
declare const AccButton: FC<AccButtonProps>;
export default AccButton;
