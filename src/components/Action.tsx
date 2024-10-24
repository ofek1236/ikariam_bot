import React from 'react';

type ActionProps = {
    buildingName: string;
    newLevel: number;
    timeToBuild: string;
    endTime: string;
};
const Action = ({ buildingName, newLevel, timeToBuild, endTime}: ActionProps) => {
    return (
        <>
        <h1>building name is {buildingName}, new level is {newLevel}, time to build is {timeToBuild} end time is {endTime} </h1>
        </>
    );
};

export default Action;