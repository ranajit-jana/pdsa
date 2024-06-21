import React from 'react';
import { Layout, theme } from 'antd';
import Navbar from '../components/Navbar';

const { Header, Content, Footer, Sider } = Layout;

const MainLayout = ({ children }) => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Navbar />
      <Layout>
        <Header style={{ padding: 0, background: "#001529" }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ color: '#e4951e', fontSize: '25px', marginLeft: '30px' }}>
              PII Detection and Sensitivity Analyzer (PDSA)
            </div>
          </div>
        </Header>
        <Content style={{ margin: '10px 10px' }}>
          <div
            style={{
              padding: 15,
              minHeight: 340,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            {children}
          </div>
        </Content>
        <Footer style={{ textAlign: 'center', padding: '8px' }}>
          PDSA ©{new Date().getFullYear()}
        </Footer>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
