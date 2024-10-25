import React from 'react';
import {Button} from 'antd';
import '../../css/ActionQueue/ActionItem.css';
import ActionItemProps from "../../interfaces/ActionItemPropsInterface.tsx";


const ActionItem: React.FC<ActionItemProps> = ({name, image, level, onAdd}) => {
    return (
        <div className="action-item-container">
            {/* Image with name underneath */}
            <div className="action-item-image-container">
                <img src={image} alt={name} className="action-item-image"/>
                <div>{name}</div>
            </div>

            {/* Level indicator on the right */}
            <div className="action-item-level">{level}</div>

            {/* Button to add to the queue */}
            {onAdd && (<Button className="action-item-button" onClick={onAdd}>
                Add
            </Button>)}
        </div>
    );
};

export default ActionItem;
