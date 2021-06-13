import axios from "axios";
import {authConfig, config, withLogs} from "../shared";
import {NoteProps} from "./NoteProps";
import {CommentProps} from "./CommentProps";
export const baseUrl = 'localhost:5000';
const scansUrl = `http://${baseUrl}/api/scans/`;
const notesUrl = `http://${baseUrl}/api/notes/`;
const commentsUrl = `http://${baseUrl}/api/comments/`;

export interface AuthProps {
    accessToken: string;
    tokenType: string;
    message: string;
}

export interface ScanProps {
    id: number,
    username: string,
    name: string,
    fileid: number
}

export const uploadConfig = (token?: string) => ({
    headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}`,
    },
});

export const getScans: (token?: string) => Promise<ScanProps[]> = (token) => {
    var getScansUrl = scansUrl + 'get'
    return withLogs(axios.get(getScansUrl, authConfig(token)), 'getScans');
}

export const uploadFile: (token: string, file: FormData) => Promise<ScanProps> = (token, file) => {
    var uploadUrl = scansUrl + 'add';
    return withLogs(axios.post(uploadUrl, file, uploadConfig(token)), "uploadFile");
}

export const saveNotesApi: (token: string, text: string, scanid: number) => Promise<NoteProps> = (token, text, scanid) => {
    var saveUrl = notesUrl + 'add/' + `${scanid}`;
    return withLogs(axios.post(saveUrl, {text}, authConfig(token)), 'saveNote');
}

export const getNotesApi: (token: string, scanid: number) => Promise<NoteProps> = (token, scanid) => {
    var getUrl = notesUrl + 'get/' + `${scanid}`;
    return withLogs(axios.get(getUrl, authConfig(token)), 'getNote');
}

export const saveCommentsApi: (token: string, text: string, scanid: number) => Promise<CommentProps> = (token, text, scanid) => {
    var saveUrl = commentsUrl + 'add/' + `${scanid}`;
    return withLogs(axios.post(saveUrl, {text}, authConfig(token)), 'saveNote');
}

export const getCommentsApi: (token: string, scanid: number) => Promise<CommentProps[]> = (token, scanid) => {
    var getUrl = commentsUrl + 'get/' + `${scanid}`;
    return withLogs(axios.get(getUrl, authConfig(token)), 'getNote');
}
