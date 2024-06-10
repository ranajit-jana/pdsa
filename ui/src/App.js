// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Page1 from './pages/Page1';
import Page2 from './pages/Page2';
import Page3 from './pages/Page3';
import MainLayout from './Layout/MainLayout';

const App = () => {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/Page1" element={<Page1 />} />
          <Route path="/Page2" element={<Page2 />} />
          <Route path="/Page3" element={<Page3 />} />
        </Routes>
      </MainLayout>
    </Router>
  );
};

export default App;
