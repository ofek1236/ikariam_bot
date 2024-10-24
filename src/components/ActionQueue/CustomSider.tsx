import React from 'react';
import { Layout, List } from 'antd';
import ActionItem from './ActionItem';

const { Sider } = Layout;

interface ComponentItem {
  name: string;
  id: number;
  data: string;
  image: string;
  level: string;
}

interface SiderProps {
  addToQueue: (component: ComponentItem) => void;
}

const componentsList: ComponentItem[] = [
  { name: 'Component 1', id: 1, data: 'Data 1', image: 'https://via.placeholder.com/50', level: '2 → 3' },
  { name: 'Component 2', id: 2, data: 'Data 2', image: 'https://via.placeholder.com/50', level: '3 → 4' },
  { name: 'Component 3', id: 3, data: 'Data 3', image: 'https://via.placeholder.com/50', level: '4 → 5' },
];

const CustomSider: React.FC<SiderProps> = ({ addToQueue }) => {
  return (
    <Sider width={250} style={{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0 }}>
      <List
        dataSource={componentsList}
        renderItem={(item) => (
          <List.Item>
            <ActionItem
              name={item.name}
              image={item.image}
              level={item.level}
              onAdd={() => addToQueue(item)}
            />
          </List.Item>
        )}
      />
    </Sider>
  );
};

export default CustomSider;
