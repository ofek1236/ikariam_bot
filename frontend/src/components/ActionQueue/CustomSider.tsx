import React from 'react';
import {Layout, List} from 'antd';
import ActionItem from './ActionItem';
import ActionItemProps from "../../interfaces/ActionItemPropsInterface.tsx";
import '../../css/ActionQueue/ActionItem.css';
const {Sider} = Layout;


interface SiderProps {
    addToQueue: (component: ActionItemProps) => void;
    componentsList: ActionItemProps[];
}

const CustomSider: React.FC<SiderProps> = ({addToQueue, componentsList}) => {
    return (
        <Sider width={250} className={"sider"}>
            <List
                dataSource={componentsList}
                renderItem={(item) => (
                    <List.Item>
                        <ActionItem
                            name={item.name}
                            image={item.image}
                            level={item.level}
                            endLevel={item.endLevel}
                            onAdd={() => addToQueue(item)}
                        />
                    </List.Item>
                )}
            />
        </Sider>
    );
};

export default CustomSider;
