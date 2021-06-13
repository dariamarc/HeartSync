import React, {useCallback, useContext, useEffect, useReducer, useState} from "react";
import PropTypes from "prop-types";
import {AuthContext} from "../auth/AuthProvider";
import {getCommentsApi, getNotesApi, getScans, saveCommentsApi, saveNotesApi, uploadFile} from "./ScanApi";
import {ScanProps} from "./ScanProps";
import {getLogger} from "../shared";
import {getFile} from "../file/fileApi";
import {CommentProps} from "./CommentProps";
const log = getLogger("ScanProvider")

export type SaveScanFn = (file: FormData) => void;
export type DownloadFileFn = (fileid: number) => void
export type SaveNotesFn = (scanid: number, text: string) => void
export type GetNotesFn = (scanid: number) => void
export type SaveCommentFn = (scanid: number, text: string) => void
export type GetCommentsFn = (scanid: number) => void

export interface ScansState {
    scans?: ScanProps[],
    notes?: string,
    comments?: CommentProps[],
    fetching: boolean,
    fetchingError?: Error | null,
    saveScan?: SaveScanFn,
    saving: boolean,
    savingError?: Error | null,
    downloadFile?: DownloadFileFn,
    downloading: boolean,
    downloadingError?: Error | null,
    saveNote?: SaveNotesFn,
    savingNote: boolean,
    savingNoteError?: Error | null,
    getNotes?: GetNotesFn,
    fetchingNotes: boolean,
    fetchingNotesError?: Error | null
    getComments?: GetCommentsFn,
    fetchingComments: boolean,
    fetchingCommentsError?: Error | null
    saveComment?: SaveCommentFn,
    savingComment: boolean,
    savingCommentError?: Error | null
}

interface ActionProps {
    type: string,
    payload?: any
}

const initialState: ScansState = {
    fetching: false,
    saving: false,
    downloading: false,
    savingNote: false,
    fetchingNotes: false,
    savingComment: false,
    fetchingComments: false
}


const FETCH_SCANS_STARTED = 'FETCH_SCANS_STARTED'
const FETCH_SCANS_SUCCEEDED = 'FETCH_SCANS_SUCCEEDED'
const FETCH_SCANS_FAILED = 'FETCH_SCANS_FAILED'
const SAVE_SCAN_STARTED = 'SAVE_SCAN_STARTED'
const SAVE_SCAN_SUCCEEDED = 'SAVE_SCAN_SUCCEEDED'
const SAVE_SCAN_FAILED = 'SAVE_SCAN_FAILED'
const FETCH_NOTES_STARTED = 'FETCH_NOTES_STARTED'
const FETCH_NOTES_SUCCEDED = 'FETCH_NOTES_SUCCEEDED'
const FETCH_NOTES_FAILED = 'FETCH_NOTES_FAILED'
const SAVE_NOTES_STARTED = 'SAVE_NOTES_STARTED'
const SAVE_NOTES_SUCCEEDED = 'SAVE_NOTES_SUCCEEDED'
const SAVE_NOTES_FAILED = 'SAVE_NOTES_FAILED'
const FETCH_COMMENTS_STARTED = 'FETCH_COMMENTS_STARTED'
const FETCH_COMMENTS_SUCCEDED = 'FETCH_COMMENTS_SUCCEEDED'
const FETCH_COMMENTS_FAILED = 'FETCH_COMMENTS_FAILED'
const SAVE_COMMENT_STARTED = 'SAVE_COMMENT_STARTED'
const SAVE_COMMENT_SUCCEEDED = 'SAVE_COMMENT_SUCCEEDED'
const SAVE_COMMENT_FAILED = 'SAVE_COMMENT_FAILED'

const reducer: (state: ScansState, action: ActionProps) => ScansState = (
    state, {type, payload}) => {
        console.log(type);
        switch(type){
            case FETCH_SCANS_STARTED:
                console.log("Fetch scans started");
                return {...state, fetching: true, fetchingError: null};
            case FETCH_SCANS_SUCCEEDED:
                console.log("Fetch scans succeeded");
                return {...state, fetching: false, scans:payload.scans};
            case FETCH_SCANS_FAILED:
                console.log("Fetch scans failed");
                return {...state, fetching: false, fetchingError: payload.error};
            case SAVE_SCAN_STARTED:
                console.log("Save scan started");
                return {...state, saving: true, savingError: null};
            case SAVE_SCAN_SUCCEEDED:
                console.log("Save scan succeded");
                const scans = [...(state.scans || [])];
                const scan = payload.scan;
                const index = scans.findIndex(it => it.id === scan.id);
                if (index === -1) {
                    scans.splice(0, 0, scan);
                } else {
                    scans[index] = scan;
                }
                return {...state, saving: false, scans: scans};
            case SAVE_SCAN_FAILED:
                console.log("Save scan failed");
                return {...state, saving: false, savingError: payload.error}
            case FETCH_NOTES_STARTED:
                return {...state, fetchingNotes: true, fetchingNotesError: null}
            case FETCH_NOTES_SUCCEDED:
                return {...state, notes: payload.notesText, fetchingNotes: false}
            case FETCH_NOTES_FAILED:
                return {...state, fetchingNotesError: payload.error, fetchingNotes: false}
            case FETCH_COMMENTS_STARTED:
                return {...state, fetchingComments: true, fetchingCommentsError: null}
            case FETCH_COMMENTS_SUCCEDED:
                return {...state, comments: payload.comments}
            case FETCH_COMMENTS_FAILED:
                return {...state, fetchingComments: false, fetchingCommentsError: payload.error}
            case SAVE_COMMENT_STARTED:
                return {...state, savingComment: true, savingCommentError: null}
            case SAVE_COMMENT_SUCCEEDED:
                console.log("Save comment succeded");
                const comments = [...(state.comments || [])];
                const comment = payload.comment;
                const index2 = comments.findIndex(it => it.id === comment.id);
                if (index2 === -1) {
                    comments.splice(0, 0, comment);
                } else {
                    comments[index2] = comment;
                }
                comments.sort((x, y) => (x.id - y.id));
                return {...state, saving: false, comments: comments};
            case SAVE_COMMENT_FAILED:
                return {...state, savingComment: false, savingCommentError: payload.error}
            case SAVE_NOTES_STARTED:
                return {...state, savingNote: true, savingNoteError: null}
            case SAVE_NOTES_SUCCEEDED:
                return {...state, savingNote: false}
            case SAVE_NOTES_FAILED:
                return {...state, savingNote: false, savingNoteError: payload.error}
            default:
                return state;
        }
};

export const ScansContext = React.createContext<ScansState>(initialState);

interface ScansProviderProps {
    children: PropTypes.ReactNodeLike
}

export const ScanProvider: React.FC<ScansProviderProps> = ({children}) => {
    let {token} = useContext(AuthContext);
    const [state, dispatch] = useReducer(reducer, initialState);
    const {scans, notes, comments, fetching, fetchingError, saving, savingError, downloading, downloadingError, savingNote
    , fetchingComments, fetchingCommentsError, fetchingNotesError, fetchingNotes, savingComment, savingCommentError, savingNoteError} = state;
    useEffect(getScansEffect, [token]);
    const saveScan = useCallback<SaveScanFn>(saveScanCallback, [token]);
    const downloadFile = useCallback<DownloadFileFn>(downloadFileCallback, [token]);
    const saveNote = useCallback<SaveNotesFn>(saveNotesCallback, [token]);
    const getNotes = useCallback<GetNotesFn>(getNotesCallback, [token]);
    const saveComment = useCallback<SaveCommentFn>(saveCommentCallback, [token]);
    const getComments = useCallback<GetCommentsFn>(getCommentsCallback, [token]);

    const value = {scans, notes, comments, saveComment, getComments, saveNote, getNotes,
        fetching, fetchingError, saving, savingError, saveScan, downloadFile, downloading, downloadingError,
        savingNote, savingComment, savingCommentError, savingNoteError, fetchingNotes, fetchingNotesError,
        fetchingComments, fetchingCommentsError};

    log('returns');
    return (
        <ScansContext.Provider value={value}>
            {children}
        </ScansContext.Provider>
    );

    function getScansEffect(){
        let canceled = false;

        fetchScans();
        return () => {
            canceled = true;
        }

        async function fetchScans() {
            if(!token?.trim()){
                return;
            }
            log('fetchScans started');
            dispatch({type: FETCH_SCANS_STARTED});
            try {
                const scans = await getScans(token);

                if (!canceled) {
                    dispatch({type: FETCH_SCANS_SUCCEEDED, payload: {scans: scans}});
                }
            }
            catch (e) {
                log('fetchScans failed');
                dispatch({type: FETCH_SCANS_FAILED, payload: {error: e}});
            }
        }
    }


    async function saveScanCallback(file: FormData){
        try{
            console.log("Save scan started");
            dispatch({type: SAVE_SCAN_STARTED});

            const response = await uploadFile(token, file);

            dispatch({type: SAVE_SCAN_SUCCEEDED, payload: {scan: response}});
        }
        catch (e) {
            dispatch({type: SAVE_SCAN_FAILED, payload: {error: e}});

        }
    }

    async function saveNotesCallback(scanid: number, text: string){
        try{
            console.log("Save note started");

            dispatch({type: SAVE_NOTES_STARTED});

            const response = await saveNotesApi(token, text, scanid);

            dispatch({type: SAVE_SCAN_SUCCEEDED, payload: {scan: response}});
        }
        catch (e) {
            dispatch({type: SAVE_NOTES_FAILED, payload: {error: e}});

        }
    }

    async function getNotesCallback(scanid: number){
        try{
            console.log("Save note started");

            dispatch({type: FETCH_NOTES_STARTED});
            const response = await getNotesApi(token, scanid);
            console.log(response);
            console.log(response.text)

            dispatch({type: FETCH_NOTES_SUCCEDED, payload: {notesText: response.text}});
        }
        catch (e) {
            dispatch({type: FETCH_NOTES_FAILED, payload: {error: e}});

        }
    }

    async function saveCommentCallback(scanid: number, text: string){
        try{
            console.log("Save note started");
            dispatch({type: SAVE_COMMENT_STARTED});
            const response = await saveCommentsApi(token, text, scanid);

            dispatch({type: SAVE_COMMENT_SUCCEEDED, payload: {comment: response}});
        }
        catch (e) {
            dispatch({type: SAVE_COMMENT_FAILED, payload: {error: e}});

        }
    }

    async function getCommentsCallback(scanid: number){
        try{
            console.log("Save note started");
            dispatch({type: FETCH_COMMENTS_STARTED});

            const response = await getCommentsApi(token, scanid);

            dispatch({type: FETCH_COMMENTS_SUCCEDED, payload: {comments: response}});
        }
        catch (e) {
            dispatch({type: FETCH_COMMENTS_FAILED, payload: {error: e}});

        }
    }

    function base64ToArrayBuffer(base64: string) {
        console.log("here")
        const binary_string = window.atob(base64);
        const len = binary_string.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binary_string.charCodeAt(i);
        }

        return bytes.buffer;
    }

    function downloadLink(content: SharedArrayBuffer | ArrayBuffer, type: any, fileName: string) {
        const link = document.createElement('a');
        const blob = new Blob([content], type);
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName.toString();
        link.click();
    }

    async function downloadFileCallback(scanid){
        try {
            log(`download started`);

            const response = await getFile(token, scanid);
            let type = {type: "model/obj"};

            let content = base64ToArrayBuffer(response.content || "");

            downloadLink(content, type, response.name);
            log('download succeeded');
        } catch (error) {
            log('download failed');
            if (error.response && error.response.status === 417) {
                error = {message: "File not found"};
            }
        }
    }
}
