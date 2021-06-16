import {ScanProps} from "./ScanProps";
import React from "react";
import {IonCardContent, IonCardTitle, IonItem} from "@ionic/react";
import './ScansHome.css';

interface ScanPropsExt extends ScanProps {
    onClick: (id?: string) => void
}

const Scan: React.FC<ScanPropsExt> = ({id, name, username, fileid, onClick}) => {

    return (
        <IonItem className="item" onClick={() => onClick(id)}>
            <IonCardContent>
                <IonCardTitle>{name}</IonCardTitle>
            </IonCardContent>
        </IonItem>
    )
}

export default Scan;