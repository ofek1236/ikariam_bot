import React from 'react';
import { Layout, List, Space } from 'antd';
import '../../css/QueueContent/QueueContent.css';
import { CloseOutlined } from '@ant-design/icons';
import ActionItemProps from "../../interfaces/ActionItemPropsInterface.tsx";
import ActionItem from "./ActionItem.tsx";

const { Content } = Layout;


interface QueueContentProps {
  queue: ActionItemProps[];
  removeFromQueue: (component: ActionItemProps) => void;
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
                  <ActionItem name={item.name} image={item.image} level={item.level}></ActionItem>
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
