import React, {useCallback, useContext, useEffect, useReducer, useState} from "react";
import PropTypes from "prop-types";
import {AuthContext} from "../auth/AuthProvider";
import {getCommentsApi, saveCommentsApi} from "./CommentApi";
import {getLogger} from "../shared";
import {CommentProps} from "./CommentProps";
const log = getLogger("CommentProvider")

export type SaveCommentFn = (scanid: string, text: string) => void
export type GetCommentsFn = (scanid: string) => void

export interface CommentState {
    comments?: CommentProps[],
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

const initialState: CommentState = {
    savingComment: false,
    fetchingComments: false
}


const FETCH_COMMENTS_STARTED = 'FETCH_COMMENTS_STARTED'
const FETCH_COMMENTS_SUCCEEDED = 'FETCH_COMMENTS_SUCCEEDED'
const FETCH_COMMENTS_FAILED = 'FETCH_COMMENTS_FAILED'
const SAVE_COMMENT_STARTED = 'SAVE_COMMENT_STARTED'
const SAVE_COMMENT_SUCCEEDED = 'SAVE_COMMENT_SUCCEEDED'
const SAVE_COMMENT_FAILED = 'SAVE_COMMENT_FAILED'

const reducer: (state: CommentState, action: ActionProps) => CommentState = (
    state, {type, payload}) => {
    switch(type){
        case FETCH_COMMENTS_STARTED:
            return {...state, fetchingComments: true, fetchingCommentsError: null}
        case FETCH_COMMENTS_SUCCEEDED:
            return {...state, comments: payload.comments}
        case FETCH_COMMENTS_FAILED:
            return {...state, fetchingComments: false, fetchingCommentsError: payload.error}
        case SAVE_COMMENT_STARTED:
            return {...state, savingComment: true, savingCommentError: null}
        case SAVE_COMMENT_SUCCEEDED:
            console.log("Save comment succeded");
            const comments = [...(state.comments || [])];
            const comment = payload.comment;
            const index = comments.findIndex(it => it.id === comment.id);
            if (index === -1) {
                comments.splice(0, 0, comment);
            } else {
                comments[index] = comment;
            }
            comments.sort((x, y) => (Date.parse(x.date) - Date.parse(y.date)));
            return {...state, saving: false, comments: comments};
        case SAVE_COMMENT_FAILED:
            return {...state, savingComment: false, savingCommentError: payload.error}
        default:
            return state;
    }
};

export var CommentContext = React.createContext<CommentState>(initialState);

interface CommentProviderProps {
    children: PropTypes.ReactNodeLike
}

export const CommentProvider: React.FC<CommentProviderProps> = ({children}) => {
    let {token} = useContext(AuthContext);
    const [state, dispatch] = useReducer(reducer, initialState);
    const {comments, fetchingComments, fetchingCommentsError, savingComment, savingCommentError} = state;
    const saveComment = useCallback<SaveCommentFn>(saveCommentCallback, [token]);
    const getComments = useCallback<GetCommentsFn>(getCommentsCallback, [token]);

    const value = {comments, saveComment, getComments, savingComment, savingCommentError, fetchingComments, fetchingCommentsError};

    log('returns');
    return (
        <CommentContext.Provider value={value}>
            {children}
        </CommentContext.Provider>
    )

    async function saveCommentCallback(scanid: string, text: string){
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

    async function getCommentsCallback(scanid: string){
        try{
            console.log("Save note started");
            dispatch({type: FETCH_COMMENTS_STARTED});

            const response = await getCommentsApi(token, scanid);

            dispatch({type: FETCH_COMMENTS_SUCCEEDED, payload: {comments: response}});
        }
        catch (e) {
            dispatch({type: FETCH_COMMENTS_FAILED, payload: {error: e}});

        }
    }

}
