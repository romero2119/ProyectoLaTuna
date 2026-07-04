import { FC } from 'react';

interface AccessibilityButtonProps {
    onShow?: () => void;
    showSpinner?: boolean;
}
declare const AccessibilityButton: FC<AccessibilityButtonProps>;
export default AccessibilityButton;
