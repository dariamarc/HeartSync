import React, {useContext, useRef, useState} from "react";
import {RouteComponentProps} from "react-router";
import {Header} from "../layout/Header";

import {
    IonButton,
    IonCard,
    IonCardContent,
    IonCardTitle,
    IonContent, IonIcon,
    IonInput, IonItem,
    IonLabel, IonList, IonLoading,
    IonPage
} from "@ionic/react";
import './ScansHome.css';
import {arrowUp, arrowUpCircleOutline, informationCircle} from "ionicons/icons";
import {ScansContext} from "./ScanProvider";
import Scan from "./Scan";

interface ScansHomeState {
    scanNo?: string
}


export const ScansHome: React.FC<RouteComponentProps> = ({history}) => {
    const {scans, fetchingError, saveScan, saving, savingError, saveScanMessage, getScan, fetchingScanError} = useContext(ScansContext);
    const [state, setState] = useState<ScansHomeState>({});
    const [scanNoError, setScanNoError] = useState<string>('')

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
        console.log("")
        setScanNoError('');
        if(state.scanNo == '' || state.scanNo == undefined){
            setScanNoError('Please enter a valid scan number');
        }
        else{
            getScan?.(state.scanNo);
            console.log(fetchingScanError);
            if (fetchingScanError === null) {
                history.push(`/scan/${state.scanNo}`);
            }
            else {
                setScanNoError('Please enter a valid scan number');
            }
        }

    }

    return (
        <IonPage>
            <Header></Header>
            <IonContent color="light">
                <IonInput placeholder='Input your scan code' onIonChange={(e) => {setState({...state, scanNo: e.detail.value || ''})}}></IonInput>
                <IonButton color="medium" shape="round" onClick={() => {handleGotoScan()}}>Go to scan</IonButton>
                {scanNoError && <div>{scanNoError}</div>}
                <div>
                    <IonCard className="upload-card">
                        <IonCardTitle className="card-center">
                            <IonIcon icon={arrowUpCircleOutline}/>
                            <h4>Upload a file now</h4>
                        </IonCardTitle>
                        <IonCardContent className="card-center">
                            <IonItem><input type='file' accept=".nii.gz" onChange={(ev) => onFileChange(ev)}></input></IonItem>
                            <IonButton color="medium" shape="round" onClick={() => submitFile()}>Submit</IonButton>
                            <IonItem>
                                <IonIcon icon={informationCircle}></IonIcon>
                                <h6 className="card-center">Accepted format: .nii.gz</h6>
                            </IonItem>
                            {savingError && (<div>{saveScanMessage}</div>)}
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