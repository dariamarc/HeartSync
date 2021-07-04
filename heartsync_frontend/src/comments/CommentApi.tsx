import axios from "axios";
import {authConfig, config, withLogs} from "../shared";
import {NoteProps} from "../notes/NoteProps";
import {CommentProps} from "../comments/CommentProps";
export const baseUrl = 'localhost:5000';

const commentsUrl = `http://${baseUrl}/api/comments/`;


export const saveCommentsApi: (token: string, text: string, scanid: string) => Promise<CommentProps> = (token, text, scanid) => {
    var saveUrl = commentsUrl + 'add/' + `${scanid}`;
    return withLogs(axios.post(saveUrl, {text}, authConfig(token)), 'saveNote');
}

export const getCommentsApi: (token: string, scanid: string) => Promise<CommentProps[]> = (token, scanid) => {
    var getUrl = commentsUrl + 'get/' + `${scanid}`;
    return withLogs(axios.get(getUrl, authConfig(token)), 'getNote');
}
