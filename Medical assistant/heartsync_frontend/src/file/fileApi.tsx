import {authConfig, withLogs} from "../shared";
import axios from "axios";

export const baseUrl = 'localhost:5000';
const filesUrl = `http://${baseUrl}/api/files/`;

interface FileResponse {
    content: string,
    name: string
}

export const fileConfig = (token?: string) => ({
    headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    }
});

export const getFile:(token: string, scanid:string) => Promise<FileResponse> = async (token, scanid) => {
    const getFileUrl = filesUrl + `get/${scanid}`;
    return withLogs(axios.get(getFileUrl, fileConfig(token)), 'getFile');
}
