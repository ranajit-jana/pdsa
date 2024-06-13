import React, { useState } from 'react';
import { DesktopOutlined, FileOutlined, PieChartOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import { Layout, Menu, Avatar } from 'antd';
import { AntDesignOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';

const { Sider } = Layout;

function getItem(label, key, icon, children, path) {
  return {
    key,
    icon,
    children,
    label: <Link to={path}>{label}</Link>,
  };
}

const items = [
  getItem('Entities', '1', <PieChartOutlined />, null, '/Page1'),
  getItem('Rules', '2', <DesktopOutlined />, null, '/Page2'),
  getItem('Score', '3', <UserOutlined />, null, '/Page3'),
];

const Navbar = () => {
  const [collapsed, setCollapsed] = useState(false);
  return (
    <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
      <div style={{ display: 'flex', justifyContent: 'center', padding: '16px' }}>
        <Avatar size={64} icon={<AntDesignOutlined />} />
      </div>
      <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={items} />
    </Sider>
  );
};

export default Navbar;
