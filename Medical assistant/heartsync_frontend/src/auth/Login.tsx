import React, {useContext, useState} from "react";
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
    const {isAuthenticated, isAuthenticating, login, authenticationError} = useContext(AuthContext)

    const handleLogin = () => {
        login?.(username, password)
    }

    if(isAuthenticated){
        return <Redirect to={{pathname: '/home'}}/>
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
                        <IonInput type="password" placeholder="Password" id="password" value={password}
                        onIonChange={e => setState({...state, password: e.detail.value || ''})}></IonInput>

                        <IonLoading isOpen={isAuthenticating}></IonLoading>
                        <IonButton color="medium" shape="round" onClick={handleLogin}>Sign in</IonButton>
                        {authenticationError && (
                            <div>{'Wrong username or password'}</div>
                        )}
                    </IonCardContent>
                </IonCard>
            </IonContent>
            <Footer></Footer>
        </IonPage>
    )
}