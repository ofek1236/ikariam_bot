import React, { useState } from 'react';
import { Layout } from 'antd';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HeaderMenu from './components/HeaderMenu';
import CustomSider from './components/ActionQueue/CustomSider';
import QueueContent from './components/ActionQueue/QueueContent';

interface ComponentItem {
  name: string;
  id: number;
}

const App: React.FC = () => {
  const [queue, setQueue] = useState<ComponentItem[]>([]);

  const removeFromQueue = (component: ComponentItem) => {
    setQueue(queue.filter((item) => item !== component));
  };
  const addToQueue = (component: ComponentItem) => {
    setQueue([...queue, component]);
  };

  return (
    <Router>
      <Layout>
        <HeaderMenu />
        <Layout>
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <CustomSider addToQueue={addToQueue} />
                  <QueueContent queue={queue} removeFromQueue={removeFromQueue} />
                </>
              }
            />
            <Route path="/page2" element={<div>Content for Page 2</div>} />
            <Route path="/page3" element={<div>Content for Page 3</div>} />
          </Routes>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App;
