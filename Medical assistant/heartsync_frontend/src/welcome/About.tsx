import React from "react";
import {RouteComponentProps} from "react-router";
import {IonCard, IonCardContent, IonCardTitle, IonIcon, IonPage} from "@ionic/react";
import {Header} from "../layout/Header";
import {heartCircleOutline} from "ionicons/icons";

export const About: React.FC<RouteComponentProps> = ({history}) => {

    return (
        <IonPage>
            <Header/>
            <IonCard className="upload-card">
                <IonCardTitle className="card-center">
                    <IonIcon icon={heartCircleOutline}/>
                    <h3>Hi there!</h3>
                </IonCardTitle>
                <IonCardContent className="card-center">
                    <h4>
                        My name is Anastasia-Daria Marc and I am soon to be graduate. HeartSync focuses on whole heart segmentation using artificial intelligence. This website will continue to grow and more features will be added, so stay tuned and happy pumping!
                    </h4>
                </IonCardContent>
            </IonCard>
        </IonPage>
    )
}