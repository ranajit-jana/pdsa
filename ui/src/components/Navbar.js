import React, { useState } from 'react';
import { DesktopOutlined, FileOutlined, PieChartOutlined, TeamOutlined, UserOutlined , BarChartOutlined} from '@ant-design/icons';
import { Layout, Menu, Avatar } from 'antd';
import { AntDesignOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Import the CSS file

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
  getItem('Entities', '1', <UserOutlined />, null, '/Page1'),
  getItem('Rules', '2', <TeamOutlined />, null, '/Page2'),
  getItem('Score', '3', <BarChartOutlined />, null, '/Page3'),
];

const Navbar = () => {
  const [collapsed, setCollapsed] = useState(false);
  return (
    <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
      <div style={{ display: 'flex', justifyContent: 'center', padding: '10px' }}>
        {collapsed ?
          (<>
            <img src="/logo.png" alt="REVA University Logo" style={{ maxWidth: '80%', height: '80%' }} />
          </>)
          :
          (<>
            <img src="/REVAUNIVERSITYLOGO.png" alt="REVA University Logo" style={{ maxWidth: '100%', height: 'auto' }} />
          </>)}
      </div>
      <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={items} className="custom-menu" />
    </Sider>
  );
};

export default Navbar;
