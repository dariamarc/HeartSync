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
        Authorization: `Bearer ${token}`,
        responseType: "arraybuffer"
    }
});

export const getFile:(token: string, fileid:number) => Promise<FileResponse> = async (token, fileid) => {
    const getFileUrl = filesUrl + `get/${fileid}`;
    return withLogs(axios.get(getFileUrl, fileConfig(token)), 'getFile');
}