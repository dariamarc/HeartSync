import React, {useContext} from "react";
import {RouteComponentProps} from "react-router";
import './Header.css';
import {
    IonButton,
    IonButtons,
    IonChip,
    IonContent,
    IonHeader,
    IonLabel,
    IonPage,
    IonTitle,
    IonToolbar
} from "@ionic/react";
import {AuthContext} from "../auth/AuthProvider";


export const Header: React.FC = () => {
    const {token, logout} = useContext(AuthContext)

    const handleLogout = () => {
        logout?.();
    }

    return (
        <>
            <IonHeader>
                <IonToolbar color="light" class="header">

                    {token != "" && (
                        <IonButtons slot="start">
                            <IonButton className="logo-button" href="/home">
                                <img className="logo-image" src="assets/logo.png" alt="heartsync_logo"/>
                            </IonButton>
                            <IonTitle class="header-title">HeartSync</IonTitle>

                        </IonButtons>
                    )}

                    {token === "" && (
                        <IonButtons slot="start">
                            <IonButton className="logo-button" href="/welcome">
                                <img className="logo-image" src="assets/logo.png" alt="heartsync_logo"/>
                            </IonButton>
                            <IonTitle class="header-title">HeartSync</IonTitle>

                        </IonButtons>
                    )}

                    {token != "" && (
                        <IonButtons slot="end">
                            <IonButton shape="round" className="header-button" onClick={handleLogout}>Logout</IonButton>
                        </IonButtons>
                    )}

                    {token === "" && (
                        <IonButtons slot="end">
                            <IonButton shape="round" className="header-button" href="#about">
                                About
                            </IonButton>
                            <IonButton shape="round" className="header-button" href="/login">
                                Sign in
                            </IonButton>
                        </IonButtons>
                    )}

                </IonToolbar>
            </IonHeader>
        </>
    )
};