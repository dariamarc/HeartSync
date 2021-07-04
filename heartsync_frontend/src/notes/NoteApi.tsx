import axios from "axios";
import {authConfig, config, withLogs} from "../shared";
import {NoteProps} from "../notes/NoteProps";
import {CommentProps} from "../comments/CommentProps";
export const baseUrl = 'localhost:5000';

const notesUrl = `http://${baseUrl}/api/notes/`;


export interface AuthProps {
    accessToken: string;
    tokenType: string;
    message: string;
}

export const saveNotesApi: (token: string, text: string, scanid: string) => Promise<NoteProps> = (token, text, scanid) => {
    var saveUrl = notesUrl + 'add/' + `${scanid}`;
    return withLogs(axios.post(saveUrl, {text}, authConfig(token)), 'saveNote');
}

export const getNotesApi: (token: string, scanid: string) => Promise<NoteProps> = (token, scanid) => {
    var getUrl = notesUrl + 'get/' + `${scanid}`;
    return withLogs(axios.get(getUrl, authConfig(token)), 'getNote');
}

