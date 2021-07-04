import React, {useContext, useEffect, useState} from "react";
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
    IonLabel, IonLoading,
    IonPage
} from "@ionic/react";
import './Login.css';
import {AuthContext} from "./AuthProvider";
import {Redirect} from "react-router-dom";

interface LoginState {
    username?: string,
    password?: string
}

export const Login: React.FC<RouteComponentProps> = ({history}) => {
    const [state, setState] = useState<LoginState>({});
    const {username, password} = state
    const {isAuthenticated, isAuthenticating, login, authenticationError, loginMessage} = useContext(AuthContext)
    const [errorUsername, setErrorUsername] = useState<string>('');
    const [errorPassword, setErrorPassword] = useState<string>('');

    const handleLogin = () => {
        setErrorUsername('');
        setErrorPassword('');
        validateUsername(username || '');
        validatePassword(password || '');
        if(errorUsername.length == 0 && errorPassword.length == 0){
            login?.(username, password)
        }
    }

    if(isAuthenticated){
        return <Redirect to={{pathname: '/home'}}/>
    }

    function validateUsername(username){
        if(username == '' || username == null) {
            setErrorUsername('Username is invalid');
        }
    }

    function validatePassword(password){
        if(password == '' || password == null){
            setErrorPassword('Password is invalid');
        }
    }

    return (
        <IonPage>
            <Header></Header>
            <IonContent color="light">
                <IonCard className="login-card">
                    <IonCardTitle className="card-center">
                        <h4>Sign in</h4>
                    </IonCardTitle>
                    <IonCardContent className="card-center">
                        <IonInput placeholder='Username' id="email" value={username}
                        onIonChange={e => setState({...state, username: e.detail.value || ''})}></IonInput>
                        {errorUsername && <div>{errorUsername}</div>}
                        <IonInput type="password" placeholder="Password" id="password" value={password}
                        onIonChange={e => setState({...state, password: e.detail.value || ''})}></IonInput>
                        {errorPassword && <div>{errorPassword}</div>}
                        <IonLoading isOpen={isAuthenticating}></IonLoading>
                        <IonButton color="medium" shape="round" onClick={handleLogin}>Sign in</IonButton>
                        {authenticationError && (
                            <div>{loginMessage}</div>
                        )}
                    </IonCardContent>
                </IonCard>
            </IonContent>
            <Footer></Footer>
        </IonPage>
    )
}