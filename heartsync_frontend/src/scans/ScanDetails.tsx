import React, {useEffect, useState, useContext} from "react";
import {RouteComponentProps} from "react-router";
import {Header} from "../layout/Header";
import {Footer} from "../layout/Footer";
import {
    IonButton, IonButtons,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle, IonCol,
    IonContent, IonGrid,
    IonInput,
    IonLabel, IonList,
    IonPage, IonRow, IonText, IonTextarea, IonTitle
} from "@ionic/react";
import "./ScanDetails.css"
import {ScansContext} from "./ScanProvider";
import Comment from "../comments/Comment";
import {CommentContext} from "../comments/CommentProvider";
import {FileContext} from "../file/FileProvider";
import {NoteContext} from "../notes/NoteProvider";

interface ScanDetailsProps extends RouteComponentProps<{
    _scanId: string
}>{}

interface ScanDetailsState {
    notesText?: string,
    comment?: string
}

export const ScanDetails: React.FC<ScanDetailsProps> = ({history, match}) => {
    const {downloadFile, downloadingError} = useContext(FileContext);
    const {notes, saveNote, getNotes, fetchingNotesError} = useContext(NoteContext);
    const {comments, saveComment, getComments, fetchingCommentsError, savingCommentError} = useContext(CommentContext);
    const [state, setState] = useState<ScanDetailsState>({})
    const {notesText, comment} = state
    const [errorComment, setErrorComment] = useState('')

    function getShareLink(){
        const url = match.params._scanId;
        navigator.clipboard.writeText(url);
        alert("Your scan code was copied to clipboard");
    }

    useEffect(() => {
        getNotes?.(match.params._scanId);

        if(fetchingNotesError){
            history.push('/home');
        }
        // setState({...state, notesText: notes || ''});
        var n = document.getElementById("notesArea")
           if(n){n.setAttribute("value", notes || '');}

    }, [notes])

    useEffect(() => {
        var commentsProv = getComments?.(match.params._scanId);
        if(fetchingCommentsError){
            history.push('/home');
        }
    }, [])


    function handleSaveNotes(){
        saveNote?.(match.params._scanId, notesText || '')
    }

    function handleSaveComment(){
        setErrorComment('');
        validateComment(comment || '');
        if(errorComment.length == 0) {
            saveComment?.(match.params._scanId, comment || '');
        }
    }

    function validateComment(comment){
        if(comment == ''){
            setErrorComment("Comment can't be empty");
        }
    }

    function handleDownloadFile(){
        downloadFile?.(match.params._scanId)
    }

    return (
        <IonPage className="page">
            <div className="flex-page-home">
            <Header/>
                <IonGrid className="grid-page">
                    <IonRow className="fullscreen-home">
                        <IonCol class="fullscreen-home">
                            <div className="top-column">
                                <div className="top-column">
                                    <div className="first-col">
                                <IonButton color="medium" shape="round" onClick={() => {handleDownloadFile();}}>Download your 3D model</IonButton>
                                        <IonButton color="medium" shape="round" onClick={() => {getShareLink()}}>Get share code</IonButton>
                                    </div>
                                        <div color="light" className="inside-content">
                                        <IonText><h3>What now?</h3></IonText>
                                        <div className="text-div">
                                            <p>Download your 3D model and load your downloaded file in your favourite OBJ viewer. Don't have one? Use the one proposed by us:</p>
                                            <a href="https://3dviewer.net/" target="_blank">Online 3D Viewer</a>
                                        </div>
                                    </div>
                                </div>
                                <div className="comments">
                                    <IonCard color="light">
                                        <IonCardHeader>
                                            <IonCardTitle>Comments:</IonCardTitle>
                                        </IonCardHeader>
                                        <IonCardContent>
                                            {comments && (
                                                           <IonList className="list-size">
                                                              {comments.map(({id, scanid, username, date, text}) => <Comment id={id} scanid={scanid} username={username} text={text} date={date} key={id}/>)}
                                                           </IonList>
                                                       )}
                                        </IonCardContent>
                                        <div>
                                            <IonCard>
                                                          <IonCardTitle>Add a comment</IonCardTitle>
                                                          <IonCardContent>
                                                              {errorComment && <div>Comment can't be empty.</div>}
                                                              <IonTextarea className="text-class" rows={4} onIonChange={e => setState({...state, comment: e.detail.value || ''})}></IonTextarea>
                                                               <IonButton color="medium" shape="round" onClick={() => {handleSaveComment()}}>Add comment</IonButton>
                                                           </IonCardContent>
                                                       </IonCard>
                                        </div>
                                    </IonCard>
                                </div>
                            </div>
                        </IonCol>
                        <IonCol>
                            <div className="first-col">
                                <IonCardTitle><h5>Notes:</h5></IonCardTitle>
                            </div>
                            <div className="">
                                <IonCardContent>
                                       <IonTextarea rows={20} id="notesArea" className="text-class" onIonChange={e => setState({...state, notesText: e.detail.value || ''})}></IonTextarea>
                                       <IonButton color="medium" shape="round" onClick={() => {handleSaveNotes()}}>Save notes</IonButton>
                                       </IonCardContent>
                            </div>
                        </IonCol>
                    </IonRow>
                    {/*<IonRow className="fullscreen-home">*/}
                    {/*    <IonCol className="fullscreen-home">*/}
                    {/*        <div>*/}

                    {/*        </div>*/}
                    {/*    </IonCol>*/}
                    {/*</IonRow>*/}
                </IonGrid>

            {/*<IonContent>*/}
            {/*<div color="light" className="top-content">*/}
            {/*<IonContent color="light" className="left-content">*/}

            {/*        <IonButton color="medium" shape="round" onClick={() => {handleDownloadFile();}}>Download your model</IonButton>*/}
            {/*        <IonButton color="medium" shape="round" onClick={() => {getShareLink()}}>Get scan number</IonButton>*/}

            {/*    <IonContent color="light" className="inside-content">*/}
            {/*        <IonText><h3>What now?</h3></IonText>*/}
            {/*        <IonText><p>Download your 3D model and load your downloaded file in your favourite OBJ viewer. Don't have one? Use </p> <a href="https://3dviewer.net/" target="_blank">Online 3D Viewer</a></IonText>*/}
            {/*    </IonContent>*/}

            {/*</IonContent>*/}
            {/*<IonContent  className="right-content">*/}
            {/*    <IonCard color="light" className="inside-content-right">*/}
            {/*        <IonCardTitle><h5>My notes:</h5></IonCardTitle>*/}
            {/*        <IonCardContent>*/}
            {/*            <IonTextarea id="notesArea" className="text" onIonChange={e => setState({...state, notesText: e.detail.value || ''})}></IonTextarea>*/}
            {/*            <IonButton color="medium" shape="round" onClick={() => {handleSaveNotes()}}>Save notes</IonButton>*/}
            {/*        </IonCardContent>*/}
            {/*    </IonCard>*/}
            {/*</IonContent>*/}
            {/*</div>*/}
            {/*<div className="bottom-content">*/}
                {/*<IonCard>*/}
                {/*    <IonCardTitle><h5>Comments:</h5></IonCardTitle>*/}
                {/*    <IonCardContent>*/}
                {/*            {comments && (*/}
                {/*                <IonList>*/}
                {/*                    {comments.map(({id, scanid, username, date, text}) => <Comment id={id} scanid={scanid} username={username} text={text} date={date} key={id}/>)}*/}
                {/*                </IonList>*/}
                {/*            )}*/}
                {/*        <IonCard>*/}
                {/*            <IonCardTitle>Add a comment</IonCardTitle>*/}
                {/*            <IonCardContent>*/}
                {/*                {errorComment && <div>Comment can't be empty.</div>}*/}
                {/*                <IonTextarea onIonChange={e => setState({...state, comment: e.detail.value || ''})}></IonTextarea>*/}
                {/*                <IonButton color="medium" shape="round" onClick={() => {handleSaveComment()}}>Add comment</IonButton>*/}
                {/*            </IonCardContent>*/}
                {/*        </IonCard>*/}
                {/*    </IonCardContent>*/}
                {/*</IonCard>*/}
            {/*</div>*/}
            {/*</IonContent>*/}
            {/*<Footer></Footer>*/}
            </div>
        </IonPage>
    )
}
