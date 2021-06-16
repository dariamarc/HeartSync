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
    IonLabel,
    IonPage
} from "@ionic/react";
import './Signup.css';
import {SignUpContext} from "./AuthProvider";
import {Redirect} from "react-router-dom";

interface SignUpState {
    email?: string;
    firstname?: string;
    lastname?: string;
    username?: string;
    password?: string;
    repeat_password?: string;
}

export const Signup: React.FC<RouteComponentProps> = ({history}) => {

    const {isSigned, isSigning, signup, signupError, signupMessage} = useContext(SignUpContext);
    const [state, setState] = useState<SignUpState>({});
    const {email, firstname, lastname, username, password, repeat_password} = state;
    const [errorUsername, setErrorUsername] = useState('');
    const [errorEmail, setErrorEmail] = useState('');
    const [errorFirstName, setErrorFirstName] = useState('');
    const [errorLastName, setErrorLastName] = useState('');
    const [errorPassword, setErrorPassword] = useState('');
    const [errorRepeatPassword, setErrorRepeatPassword] = useState('');

    const handleSignUp = () => {
        setErrorUsername('');
        setErrorFirstName('');
        setErrorLastName('');
        setErrorEmail('');
        setErrorPassword('');
        setErrorRepeatPassword('');
        validateUsername(username || '');
        validateEmail(email || '');
        validateFirstName(firstname || '');
        validateLastName(lastname || '');
        validatePassword(password || '');
        validateRepeatPassword(password || '');
        if (errorEmail.length == 0 && errorFirstName.length == 0 && errorLastName.length == 0 && errorPassword.length == 0 && errorRepeatPassword.length == 0 && errorUsername.length == 0) {
            signup?.(username, password, email, firstname, lastname);
        }
    };

    if (isSigned) {
        return <Redirect to={{pathname: '/login'}}/>
    }


    function validateUsername(username: string): void {
        if (username == '' || username == undefined) {
            setErrorUsername('Username must not be empty');
        }
    }

    function validatePassword(password: string): void {
        if (password.length >= 5) {
            setErrorPassword('');
        } else if (password.length >= 3) {
            const strongRegex = new RegExp("^(?=.*[a-z])(?=.*[0-9])(?=.*[.!@#$%^&*])");
            if (strongRegex.test(password)) {
                setErrorPassword('');
            }
        } else {
            setErrorPassword('Password is not strong enough');
        }
    }

    function validateRepeatPassword(repeatPassword: string): void {
        if(repeatPassword === password){
            setErrorRepeatPassword('');
        }
        else{
            setErrorRepeatPassword('Passwords do not match');
        }
    }

    function validateEmail(email: string): void {
        if (email == '' || email == undefined) {
            setErrorEmail('Email must not be empty');
        } else if (email.indexOf('@') === -1) {
            setErrorEmail('Email must contain \'@\'');
        }
    }

    function validateFirstName(firstName: string): void {
        if (firstName == '' || firstName == undefined) {
            setErrorFirstName('Firstname must not be empty');
        }
    }

    function validateLastName(lastName: string): void {
        if (lastName == '' || lastName == undefined) {
            setErrorLastName('Lastname must not be empty');
        }
    }

    return (
        <IonPage>
            <Header/>
            <IonContent color="light">
                <IonCard className="signup-card">
                    <IonCardTitle className="card-center">
                        <h4>Sign up</h4>
                    </IonCardTitle>
                    <IonCardContent className='card-center'>
                        <IonInput placeholder="Username" value={username}
                                  onIonChange={e => setState({...state, username: e.detail.value || ''})}/>
                        {errorUsername && <div>{errorUsername}</div>}
                        <IonInput placeholder="First name" value={firstname}
                                  onIonChange={e => setState({...state, firstname: e.detail.value || ''})}/>
                        {errorFirstName && <div>{errorFirstName}</div>}
                        <IonInput placeholder="Last name" value={lastname}
                                  onIonChange={e => setState({...state, lastname: e.detail.value || ''})}/>
                        {errorLastName && <div>{errorLastName}</div>}
                        <IonInput placeholder="Email" value={email}
                                  onIonChange={e => setState({...state, email: e.detail.value || ''})}/>
                        {errorEmail && <div>{errorEmail}</div>}
                        <IonInput type="password" placeholder="Password" value={password}
                                  onIonChange={e => setState({...state, password: e.detail.value || ''})}/>
                        {errorPassword && <div>{errorPassword}</div>}
                        <IonInput type="password" placeholder="Confirm password" value={repeat_password}
                                  onIonChange={e => setState({...state, repeat_password: e.detail.value || ''})}/>
                        {errorRepeatPassword && <div>{errorRepeatPassword}</div>}
                        <IonButton color="medium" shape="round" onClick={handleSignUp}>Create account</IonButton>
                        {signupError && <div>{signupMessage}</div>}
                    </IonCardContent>
                </IonCard>
            </IonContent>
            <Footer></Footer>
        </IonPage>
    )
}