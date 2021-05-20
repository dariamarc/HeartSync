import {getLogger} from "../shared";
import React, {useCallback, useEffect, useState} from "react";
import PropTypes from "prop-types";
import { Storage } from "@capacitor/core";
import {login as loginApi, signup as signupApi} from './AuthApi'
const log = getLogger('AuthProvider')

type LoginFn = (username?: string, password?: string) => void
type LogoutFn = () => void
type SignUpFn = (username?: string, password?: string, email?: string, firstname?: string, lastname?: string) => void

export interface AuthState {
    authenticationError: Error | null;
    isAuthenticated: boolean;
    isAuthenticating: boolean;
    login?: LoginFn;
    logout? : LogoutFn;
    pendingAuthentication?: boolean;
    username?: string;
    password?: string;
    token: string;
}

export interface SignUpState {
    signupError: Error | null;
    isSigned: boolean;
    isSigning: boolean;
    signup?: SignUpFn;
    pendingSigning: boolean;
    username?: string;
    password?: string;
    firstname?: string;
    lastname?: string;
    email?: string;
    message: string | null;
}

const initialState: AuthState = {
    isAuthenticated: false,
    isAuthenticating: false,
    authenticationError: null,
    pendingAuthentication: false,
    token: '',
};

const signUpInitialState: SignUpState = {
    isSigned: false,
    isSigning: false,
    signupError: null,
    pendingSigning: false,
    message: null,
}

export const AuthContext = React.createContext<AuthState>(initialState);
export const SignUpContext = React.createContext<SignUpState>(signUpInitialState);

interface AuthProviderProps {
    children: PropTypes.ReactNodeLike
}

export const AuthProvider: React.FC<AuthProviderProps> = ({children}) => {
    const [signUpState, setSignUpState] = useState<SignUpState>(signUpInitialState)
    const {isSigned, isSigning, signupError, pendingSigning, message} = signUpState
    const signup = useCallback<SignUpFn>(signupCallback, [])
    useEffect(signupEffect, [pendingSigning])
    const valueS = {isSigned, signup, isSigning, signupError, pendingSigning, message}

    const [state, setState] = useState<AuthState>(initialState);
    const { isAuthenticated, isAuthenticating, authenticationError, pendingAuthentication, token } = state;
    const login = useCallback<LoginFn>(loginCallback, []);
    const logout = useCallback<LogoutFn>(logoutCallback, []);
    useEffect(authenticationEffect, [pendingAuthentication]);

    const value = { isAuthenticated, login, logout, isAuthenticating, authenticationError, token};

    log('render');
    return (
        <SignUpContext.Provider value = {valueS}>
            <AuthContext.Provider value={value}>
                {children}
            </AuthContext.Provider>
        </SignUpContext.Provider>
    );

    function signupCallback(username?: string, password?: string, email?: string, firstname?: string, lastname?: string): void {
        log('sign up');
        setSignUpState({
            ...signUpState,
            pendingSigning: true,
            username,
            password,
            firstname,
            lastname,
            email,
            message
        });
    }

    function loginCallback(username?: string, password?: string): void {
        log('login');
        setState({
            ...state,
            pendingAuthentication: true,
            username,
            password
        });
    }

    function logoutCallback(): void {
        log('logout');
        (async () => {
            await Storage.set({
                key: 'token',
                value: ''
            });
            setState({
                ...state,
                token: '',
                isAuthenticated: false,
            });

        })();
    }

    function signupEffect() {
        let canceled = false;
        sign();
        return () => {
            canceled = true;
        }

        async function sign() {
            if (!pendingSigning) {
                log('sign, !pendingSigning, return');
                return;
            }
            try {
                log('Signing...');
                setSignUpState({
                    ...signUpState,
                    isSigning: true,
                });
                const { username, password, firstname, lastname, email } = signUpState;
                const {message} = await signupApi(username, password, email, firstname, lastname);
                //console.log(message)
                if (canceled) {
                    return;
                }
                log('Sign Up succeeded');
                if(message != "") {
                    setSignUpState({
                        ...signUpState,
                        pendingSigning: false,
                        isSigned: true,
                        isSigning: false,
                    });
                }
                else {
                    setSignUpState({
                        ...signUpState,
                        pendingSigning: false,
                        isSigned: false,
                        isSigning: false,
                        message: message,
                    });
                }
            } catch (error) {
                if (canceled) {
                    return;
                }
                log('Sign Up failed');
                setSignUpState({
                    ...signUpState,
                    signupError: error,
                    pendingSigning: false,
                    isSigning: false,
                    message: null,
                });
            }
        }
    }

    function authenticationEffect() {
        let canceled = false;
        authenticate();

        return () => {
            canceled = true;
        }

        async function authenticate() {

            var token = await Storage.get({ key: 'token' });
            console.log(token.value)

            if(token.value && token.value != '' && token.value != undefined){
                console.log(token.value)
                setState({
                    ...state,
                    token: token.value,
                    pendingAuthentication: false,
                    isAuthenticated: true,
                    isAuthenticating: false,
                });
            }

            if (!pendingAuthentication) {
                log('authenticate, !pendingAuthentication, return');
                return;
            }
            try {
                log('authenticate...');
                setState({
                    ...state,
                    isAuthenticating: true,
                });
                const { username, password } = state;
                const { accessToken } = await loginApi(username, password);
                const token = accessToken;
                console.log("Token= ",token)
                if (canceled) {
                    return;
                }
                log('authenticate succeeded');
                await Storage.set({
                    key: 'token',
                    value: token
                });
                setState({
                    ...state,
                    token,
                    pendingAuthentication: false,
                    isAuthenticated: true,
                    isAuthenticating: false,
                });
            } catch (error) {
                if (canceled) {
                    return;
                }
                log('authenticate failed');
                setState({
                    ...state,
                    authenticationError: error,
                    pendingAuthentication: false,
                    isAuthenticating: false,
                });
            }
        }
    }
};