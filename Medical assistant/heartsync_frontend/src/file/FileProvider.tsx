import React, {useCallback, useContext, useEffect, useReducer, useState} from "react";
import PropTypes from "prop-types";
import {AuthContext} from "../auth/AuthProvider";
import {getLogger} from "../shared";
import {getFile} from "../file/fileApi";
const log = getLogger("FileProvider")

export type DownloadFileFn = (fileid: string) => void


export interface FileState {
    downloadFile?: DownloadFileFn,
    downloading: boolean,
    downloadingError?: Error | null
}

interface ActionProps {
    type: string,
    payload?: any
}

const initialState: FileState = {
    downloading: false
}


const FETCH_FILE_STARTED = 'FETCH_FILE_STARTED'
const FETCH_FILE_SUCCEEDED = 'FETCH_FILE_SUCCEEDED'
const FETCH_FILE_FAILED = 'FETCH_FILE_FAILED'

const reducer: (state: FileState, action: ActionProps) => FileState = (
    state, {type, payload}) => {
    switch(type){
        case FETCH_FILE_STARTED:
            console.log("Fetch file started");
            return {...state, downloading: true, downloadingError: null};
        case FETCH_FILE_SUCCEEDED:
            console.log("Fetch file succeeded");
            return {...state, downloading: false};
        case FETCH_FILE_FAILED:
            console.log("Fetch file failed");
            return {...state, downloading: false, downloadingError: payload.error};
        default:
            return state;
    }
};

export const FileContext = React.createContext<FileState>(initialState);

interface FileProviderProps {
    children: PropTypes.ReactNodeLike
}

export const FileProvider: React.FC<FileProviderProps> = ({children}) => {
    let {token} = useContext(AuthContext);
    const [state, dispatch] = useReducer(reducer, initialState);
    const {downloading, downloadingError} = state;
    const downloadFile = useCallback<DownloadFileFn>(downloadFileCallback, [token]);

    const value = {downloadFile, downloading, downloadingError};

    log('returns');
    return (
        <FileContext.Provider value={value}>
            {children}
        </FileContext.Provider>
    );

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
