import { FC, ReactNode } from 'react';
import { IconSvgComponent } from '../../types';
import { CollapsedStateKeys } from '../../config';

interface AccMenuContentBlockProps {
    children: ReactNode;
    name: CollapsedStateKeys;
    onCollapse: (name: CollapsedStateKeys) => void;
    isExpanded: boolean;
    isAccMenuContentActive: boolean;
    Icon: IconSvgComponent;
    tKey: string;
}
declare const AccMenuContentBlock: FC<AccMenuContentBlockProps>;
export default AccMenuContentBlock;
