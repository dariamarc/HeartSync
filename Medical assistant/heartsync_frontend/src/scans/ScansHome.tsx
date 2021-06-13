import React, {useContext, useRef, useState} from "react";
import {RouteComponentProps} from "react-router";
import {Header} from "../layout/Header";
import {Footer} from "../layout/Footer";
import {
    IonButton,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonContent, IonIcon,
    IonInput, IonItem,
    IonLabel, IonList, IonLoading,
    IonPage
} from "@ionic/react";
import './ScansHome.css';
import {informationCircle} from "ionicons/icons";
import {ScansContext} from "./ScanProvider";
import Scan from "./Scan";

interface ScansHomeState {
    scanNo?: string
}


export const ScansHome: React.FC<RouteComponentProps> = ({history}) => {
    const {scans, fetching, fetchingError, saveScan, saving, savingError} = useContext(ScansContext);
    const [state, setState] = useState<ScansHomeState>({});

    interface InternalValues {
        file: any;
    }

    const values = useRef<InternalValues>({
        file: false,
    });

    const onFileChange = (fileChangeEvent: any) => {
        values.current.file = fileChangeEvent.target.files[0];
    };

    const submitFile = async () => {
        if (!values.current.file) {
            return false;
        }
        console.log(values.current.file)
        let formData = new FormData();
        formData.append("file", values.current.file);
        try {
                saveScan?.(formData);
        } catch (err) {
            console.log(err);
        }
    };

    function handleGotoScan(){
        history.push(`/scan/${state.scanNo}`);
    }

    return (
        <IonPage>
            <Header></Header>
            <IonContent color="light">
                <IonInput placeholder='Input scan number shared with user' onIonChange={(e) => {setState({...state, scanNo: e.detail.value || ''})}}></IonInput>
                <IonButton color="medium" shape="round" onClick={() => {handleGotoScan()}}>Go to scan</IonButton>
                <div>
                    <IonCard className="upload-card">
                        <IonCardTitle className="card-center"><h4>Upload a file now</h4></IonCardTitle>
                        <IonCardContent className="card-center">
                            <IonItem><input type='file' accept=".nii.gz" onChange={(ev) => onFileChange(ev)}></input></IonItem>
                            <IonButton color="medium" shape="round" onClick={() => submitFile()}>Submit</IonButton>
                            <IonItem>
                                <IonIcon icon={informationCircle}></IonIcon>
                                <h6 className="card-center">Accepted format: .nii.gz</h6>
                            </IonItem>
                            {savingError && (<div>Invalid file. Upload only .nii.gz format!</div>)}
                        </IonCardContent>
                    </IonCard>
                    <h6 className="card-center">or</h6>
                    <IonCard className="scans-card">
                        <IonCardTitle className="card-center"><h4>Try one of the saved models:</h4></IonCardTitle>
                        <IonCardContent>
                            {scans && (<IonList>
                                {scans.map(({id, name, username, fileid}) => <Scan onClick={() => {
                                history.push(`/scan/${id}`)}
                                } name={name} username={username} fileid={fileid} key={id}/>)}
                            </IonList>)}
                            {scans?.length==0 && (<IonItem className="card-center"><h5>You have no saved models. Upload a file to create one.</h5></IonItem>)}
                        </IonCardContent>
                    </IonCard>
                    <IonLoading isOpen={saving} message="Uploading scan. This may take a while." />
                </div>
            </IonContent>
            {/*<Footer></Footer>*/}
        </IonPage>
    )
}