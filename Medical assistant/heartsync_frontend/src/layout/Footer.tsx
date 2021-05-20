import React from "react";
import {IonFooter, IonTitle, IonToolbar} from "@ionic/react";
import './Footer.css'

export const Footer: React.FC = () => {

    return (
        <>
            <IonFooter>
                <IonToolbar color="light" class="footer">
                    <IonTitle class="bottom-text">&copy; HeartSync 2021</IonTitle>
                </IonToolbar>
            </IonFooter>
        </>
    )
}