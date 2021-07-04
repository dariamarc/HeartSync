import axios from "axios";
import {config, withLogs} from "../shared";

export const baseUrl = 'localhost:5000';

const authUrl = `http://${baseUrl}/api/auth/login`;
const singupUrl = `http://${baseUrl}/api/auth/signup`;
const confirmUrl = `http://${baseUrl}/api/auth/confirm`;

export interface AuthProps {
    accessToken: string;
    tokenType: string;
    message: string;
}

export interface ResponseProps {
    message: string;
    success: boolean;
}

export const login: (username?: string, password?: string) => Promise<AuthProps> = (username, password) => {
    return withLogs(axios.post(authUrl, {username, password}, config), 'login');
}

export const signup: (username?: string, password?: string, email?: string, firstname?: string, lastname?: string) => Promise<ResponseProps> = (username, password, email, firstname, lastname) => {
    return withLogs(axios.post(singupUrl, {username, password, email, firstname, lastname}, config), 'sign up');
}

export const confirmEmailApi: (token?: string) => Promise<ResponseProps> = (token) => {
    return withLogs(axios.post(confirmUrl, {token}, config), 'confirm');
}