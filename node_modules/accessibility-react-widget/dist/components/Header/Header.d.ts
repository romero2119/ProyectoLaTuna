import { FC } from 'react';

interface HeaderProps {
    onShow: () => void;
    onInit: () => void;
}
declare const Header: FC<HeaderProps>;
export default Header;
