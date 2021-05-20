import React from "react";
import {RouteComponentProps} from "react-router";
import {Header} from "../layout/Header";
import {Footer} from "../layout/Footer";
import {
    IonButton,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonContent,
    IonInput,
    IonLabel,
    IonPage
} from "@ionic/react";


export const ScanDetails: React.FC<RouteComponentProps> = ({history}) => {

    return (
        <IonPage>
            <Header></Header>
            <IonContent color="light">
            </IonContent>
            <Footer></Footer>
        </IonPage>
    )
}