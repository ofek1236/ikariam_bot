import React from 'react';
import { Layout, List, Space } from 'antd';
import '../../css/QueueContent/QueueContent.css';
import { CloseOutlined } from '@ant-design/icons';

const { Content } = Layout;

interface ComponentItem {
  name: string;
  id: number;
}

interface QueueContentProps {
  queue: ComponentItem[];
  removeFromQueue: (component: ComponentItem) => void;
}

const QueueContent: React.FC<QueueContentProps> = ({ queue, removeFromQueue }) => {
  return (
    <Layout style={{ marginLeft: 200 }}>
      <Content style={{ padding: '24px', minHeight: '100vh' }}>
        <h2>Queue (Top to Bottom)</h2>
        <List
          dataSource={queue}
          renderItem={(item) => (
            <List.Item>
              <Space size="large">
                <div>{item.name}</div>
                <CloseOutlined
                  onClick={() => {
                    removeFromQueue(item);
                  }}
                />
              </Space>
            </List.Item>
          )}
        />
      </Content>
    </Layout>
  );
};

export default QueueContent;
