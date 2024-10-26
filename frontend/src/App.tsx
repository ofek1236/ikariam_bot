import React, {useEffect, useState} from 'react';
import { Layout } from 'antd';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HeaderMenu from './components/HeaderMenu';
import CustomSider from './components/ActionQueue/CustomSider';
import QueueContent from './components/ActionQueue/QueueContent';
import ActionItemProps from "../../interfaces/ActionItemPropsInterface.tsx";
import QueueResponse from "../../interfaces/QueueResponseInterface.tsx";
import AcademyImage from "./assets/buildings/academy.png";
import TownHallImage from "./assets/buildings/townhall.png";
import BarracksImage from "./assets/buildings/barracks.png";
import axios from 'axios';
const App: React.FC = () => {



  const [queue, setQueue] = useState<ActionItemProps[]>([]);
  const [componentsList, setComponentsList] = useState<ActionItemProps[]>([
    {name: 'Academy', image: AcademyImage, level: 8, endLevel: 9}, /* Add Requests mocks here for later on*/
    {name: 'Town Hall', image: TownHallImage, level: 3, endLevel: 4},
    {name: 'Barracks', image: BarracksImage, level: 4, endLevel: 5},
  ]);

  useEffect(() => {
    const fetchQueue = async () => {
      try {
        const response = await axios.get<QueueResponse>('http://127.0.0.1:8000/queues/', {
          params: { username: 'ofeks' },
        });
        console.log(response.data.events)
        //setEvents(response.data.events); // Save events to state
        console.log('Events:', response.data); // Log events to console
      } catch (error) {
        console.error('Error fetching queue:', error);
      }
    };

    fetchQueue();
  }, []);


  const removeFromQueue = (component: ActionItemProps) => {
    setQueue(
        queue.filter((item) => item.name !== component.name || item.level < component.level)
    );
    setComponentsList((prevItems) =>
        prevItems.map((i) => (i.name === component.name ? {...i, endLevel: component.endLevel - 1} : i)) /* Will be removed after DB usage */
    );


  };
  const addToQueue = (component: ActionItemProps) => {
    setQueue([...queue,
      {...component, level: component.endLevel, endLevel: component.endLevel + 1}]);
    setComponentsList((prevItems) =>
        prevItems.map((i) => (i.name === component.name ? {...component, endLevel: component.endLevel + 1} : i))
    );
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
                  <CustomSider addToQueue={addToQueue} componentsList={componentsList}/>
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
