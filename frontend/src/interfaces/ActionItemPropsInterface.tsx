interface ActionItemProps {
    name: string;
    image: string;
    level: number;
    endLevel: number;
    onAdd?: () => void;
}

export default ActionItemProps;