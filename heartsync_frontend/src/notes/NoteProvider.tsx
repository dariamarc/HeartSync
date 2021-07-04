import React, {useCallback, useContext, useEffect, useReducer, useState} from "react";
import PropTypes from "prop-types";
import {AuthContext} from "../auth/AuthProvider";
import {getNotesApi, saveNotesApi} from "./NoteApi";
import {getLogger} from "../shared";

const log = getLogger("NoteProvider")

export type SaveNotesFn = (scanid: string, text: string) => void
export type GetNotesFn = (scanid: string) => void

export interface NoteState {
    notes?: string,
    saveNote?: SaveNotesFn,
    savingNote: boolean,
    savingNoteError?: Error | null,
    getNotes?: GetNotesFn,
    fetchingNotes: boolean,
    fetchingNotesError?: Error | null
}

interface ActionProps {
    type: string,
    payload?: any
}

const initialState: NoteState = {
    savingNote: false,
    fetchingNotes: false
}

const FETCH_NOTES_STARTED = 'FETCH_NOTES_STARTED'
const FETCH_NOTES_SUCCEDED = 'FETCH_NOTES_SUCCEEDED'
const FETCH_NOTES_FAILED = 'FETCH_NOTES_FAILED'
const SAVE_NOTES_STARTED = 'SAVE_NOTES_STARTED'
const SAVE_NOTES_SUCCEEDED = 'SAVE_NOTES_SUCCEEDED'
const SAVE_NOTES_FAILED = 'SAVE_NOTES_FAILED'

const reducer: (state: NoteState, action: ActionProps) => NoteState = (
    state, {type, payload}) => {
    console.log(type);
    switch(type){
        case FETCH_NOTES_STARTED:
            return {...state, fetchingNotes: true, fetchingNotesError: null}
        case FETCH_NOTES_SUCCEDED:
            return {...state, notes: payload.notesText, fetchingNotes: false}
        case FETCH_NOTES_FAILED:
            return {...state, fetchingNotesError: payload.error, fetchingNotes: false}
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

export const NoteContext = React.createContext<NoteState>(initialState);

interface NoteProviderProps {
    children: PropTypes.ReactNodeLike
}

export const NoteProvider: React.FC<NoteProviderProps> = ({children}) => {
    let {token} = useContext(AuthContext);
    const [state, dispatch] = useReducer(reducer, initialState);
    const {notes, savingNote, fetchingNotesError, fetchingNotes, savingNoteError} = state;
    const saveNote = useCallback<SaveNotesFn>(saveNotesCallback, [token]);
    const getNotes = useCallback<GetNotesFn>(getNotesCallback, [token]);

    const value = {notes, saveNote, getNotes, savingNote, savingNoteError, fetchingNotes, fetchingNotesError};

    log('returns');
    return (
        <NoteContext.Provider value={value}>
            {children}
        </NoteContext.Provider>
    );


    async function saveNotesCallback(scanid: string, text: string){
        try{
            console.log("Save note started");

            dispatch({type: SAVE_NOTES_STARTED});

            const response = await saveNotesApi(token, text, scanid);

            dispatch({type: SAVE_NOTES_SUCCEEDED, payload: {note: response}});
        }
        catch (e) {
            dispatch({type: SAVE_NOTES_FAILED, payload: {error: e}});

        }
    }

    async function getNotesCallback(scanid: string){
        try{
            console.log("Get notes started");

            dispatch({type: FETCH_NOTES_STARTED});
            const response = await getNotesApi(token, scanid);

            dispatch({type: FETCH_NOTES_SUCCEDED, payload: {notesText: response.text}});
        }
        catch (e) {
            dispatch({type: FETCH_NOTES_FAILED, payload: {error: e}});
        }
    }

}
