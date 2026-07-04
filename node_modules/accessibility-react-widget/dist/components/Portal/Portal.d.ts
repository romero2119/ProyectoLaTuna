import { ReactNode } from 'react';

interface PortalProps {
    children: ReactNode;
    wrapperElementId?: string;
    [key: string]: unknown;
}
declare const Portal: ({ children, wrapperElementId }: PortalProps) => React.ReactPortal | null;
export default Portal;
