import React from 'react';
import {RightOutlined} from "@ant-design/icons";
import AcademyImage from '../assets/buildings/academy.png';
import '../css/Action.css';

type ActionProps = {
    buildingName: string
    newLevel: number;
    timeToBuild: string;
    endTime: string;
};

const buildingImages: { [key: string]: string } = {
    academy: AcademyImage,
    default: AcademyImage, // Optional fallback image for unmatched names
};

const Action = ({buildingName, newLevel, timeToBuild, endTime}: ActionProps) => {
    const imagePath = buildingImages[buildingName] || buildingImages['default'];

    return (
        <div className="ActionContainer">
            <div className="ActionImageContainer">
                <img src={imagePath} alt={buildingName}/>
                <div>{buildingName}</div>
            </div>
            <div className={"ActionSeparator"}></div>
            <div className="ActionLevelContainer">
                {newLevel - 1} <RightOutlined/> {newLevel}
            </div>
            <div className={"ActionSeparator"}></div>
            <div className="ActionBuildTimeContainer">
                {timeToBuild} Minutes
            </div>
            <div className={"ActionSeparator"}></div>
            <div className="ActionEndTimeContainer">
                {endTime}
            </div>
        </div>
    );
};

export default Action;
