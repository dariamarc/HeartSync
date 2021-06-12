import React, {useCallback, useContext, useEffect, useReducer} from "react";
import PropTypes from "prop-types";
import {AuthContext} from "../auth/AuthProvider";
import {getScans, uploadFile} from "./ScanApi";
import {ScanProps} from "./ScanProps";
import {getLogger} from "../shared";
import {getFile} from "../file/fileApi";
import * as Util from "util";
import {Filesystem} from "@capacitor/core";
const log = getLogger("ScanProvider")

export type SaveScanFn = (file: FormData) => void;
export type DownloadFileFn = (fileid: number) => void

export interface ScansState {
    scans?: ScanProps[],
    fetching: boolean,
    fetchingError?: Error | null,
    saveScan?: SaveScanFn,
    saving: boolean,
    savingError?: Error | null,
    downloadFile?: DownloadFileFn,
    downloading: boolean,
    downloadingError?: Error | null
}

interface ActionProps {
    type: string,
    payload?: any
}

const initialState: ScansState = {
    fetching: false,
    saving: false,
    downloading: false
}

const FETCH_SCANS_STARTED = 'FETCH_SCANS_STARTED'
const FETCH_SCANS_SUCCEEDED = 'FETCH_SCANS_SUCCEEDED'
const FETCH_SCANS_FAILED = 'FETCH_SCANS_FAILED'
const SAVE_SCAN_STARTED = 'SAVE_SCAN_STARTED'
const SAVE_SCAN_SUCCEEDED = 'SAVE_SCAN_SUCCEEDED'
const SAVE_SCAN_FAILED = 'SAVE_SCAN_FAILED'

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
    const {scans, fetching, fetchingError, saving, savingError, downloading, downloadingError} = state;
    useEffect(getScansEffect, [token]);
    const saveScan = useCallback<SaveScanFn>(saveScanCallback, [token]);
    const downloadFile = useCallback<DownloadFileFn>(downloadFileCallback, [token]);

    const value = {scans, fetching, fetchingError, saving, savingError, saveScan, downloadFile, downloading, downloadingError};
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

    async function downloadFileCallback(fileid){
        try{
            console.log("Download file started");
            const response = await getFile(token, fileid);

            let options = {type: "obj"};
            let filename = response.name;
            // Util.createAndDownloadBlobFile(response.content, options, filename);
            // Filesystem.writeFile({path})
            
        }
    }
}
