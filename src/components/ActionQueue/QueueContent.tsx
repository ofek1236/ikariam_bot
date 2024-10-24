import React from 'react';
import { Layout, List } from 'antd';

const { Content } = Layout;

interface ComponentItem {
  name: string;
  id: number;
}

interface QueueContentProps {
  queue: ComponentItem[];
}

const QueueContent: React.FC<QueueContentProps> = ({ queue }) => {
  return (
    <Layout style={{ marginLeft: 200 }}>
      <Content style={{ padding: '24px', minHeight: '100vh' }}>
        <h2>Queue (Top to Bottom)</h2>
        <List
          dataSource={queue}
          renderItem={(item) => (
            <List.Item>
              <div>{item.name}</div>
            </List.Item>
          )}
        />
      </Content>
    </Layout>
  );
};

export default QueueContent;
