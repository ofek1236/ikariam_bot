// HeaderMenu.tsx
import React from 'react';
import { Menu, Layout } from 'antd';
import { NavLink } from 'react-router-dom';
import '../css/Header.css';
const { Header } = Layout;

const HeaderMenu: React.FC = () => {
    return (
        <Header>
            <Menu theme="dark" mode="horizontal">
                <Menu.Item key="1">
                    <NavLink to="/">Page 1</NavLink>
                </Menu.Item>
                <Menu.Item key="2">
                    <NavLink to="/page2">Page 2</NavLink>
                </Menu.Item>
                <Menu.Item key="3">
                    <NavLink to="/page3">Page 3</NavLink>
                </Menu.Item>
            </Menu>
        </Header>
    );
};

export default HeaderMenu;
