import React, {useContext, useEffect, useReducer} from "react";
import PropTypes from "prop-types";
import {AuthContext} from "../auth/AuthProvider";
import {getScans} from "./ScanApi";
import {ScanProps} from "./ScanProps";
import {getLogger} from "../shared";
const log = getLogger("ScanProvider")
export type SaveScanFn = (file: FormData) => void;

export interface ScansState {
    scans?: ScanProps[],
    fetching: boolean,
    fetchingError?: Error | null,
    saveScan?: SaveScanFn,
    saving: boolean,
    savingError?: Error | null
}

interface ActionProps {
    type: string,
    payload?: any
}

const initialState: ScansState = {
    fetching: false,
    saving: false
}

const FETCH_SCANS_STARTED = 'FETCH_SCANS_STARTED'
const FETCH_SCANS_SUCCEEDED = 'FETCH_SCANS_SUCCEEDED'
const FETCH_SCANS_FAILED = 'FETCH_SCANS_FAILED'

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
    const {scans, fetching, fetchingError, saving, savingError} = state;
    useEffect(getScansEffect, [token]);

    const value = {scans, fetching, fetchingError, saving, savingError};
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
}
