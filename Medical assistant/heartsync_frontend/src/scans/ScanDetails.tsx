import React, {useEffect, useMemo, useRef, useState, Suspense, lazy, useContext} from "react";
import {RouteComponentProps} from "react-router";
import {Header} from "../layout/Header";
import {Footer} from "../layout/Footer";
import {
    IonButton,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonContent,
    IonInput,
    IonLabel, IonList,
    IonPage, IonText, IonTextarea, IonTitle
} from "@ionic/react";
import {Canvas, extend, useLoader, useThree} from "@react-three/fiber";
import {Html, OrbitControls, useProgress} from "@react-three/drei";
import "./ScanDetails.css"
import {OBJLoader} from "three/examples/jsm/loaders/OBJLoader";
import {ModelView} from 'react-native-3d-model-view'
import {Group} from "three";
import {GLTFLoader} from "three/examples/jsm/loaders/GLTFLoader";
import {ObjViewer} from "react-obj-viewer"
import {ScansContext} from "./ScanProvider";

interface ScanDetailsProps extends RouteComponentProps<{
    _scanId?: string
}>{}

export const ScanDetails: React.FC<ScanDetailsProps> = ({history, match}) => {
    const {} = useContext(ScansContext);
    const [isLoaded, setIsLoaded] = useState(false);

    function getShareLink(){
        const url = 'localhost:8100' + match.url;
        navigator.clipboard.writeText(url);
        alert("Your link was copied to clipboard");
    }

    // function Model() {
    //     try {
    //         const objLoaded = useLoader(OBJLoader, require("box.obj"));
    //         console.log(objLoaded);
    //         setIsLoaded(true);
    //         return (
    //             <Suspense fallback={<Loader/>}>
    //                 {isLoaded && <primitive object={objLoaded} />}
    //                 {!isLoaded && <sphereBufferGeometry></sphereBufferGeometry>}
    //     </Suspense>)
    //     }
    //     catch (e) {
    //         console.log(e);
    //     }
    //     return null;
    // }
    //
    // function Loader() {
    //     const { progress } = useProgress()
    //     return <Html center>{progress} % loaded</Html>
    // }

    function downloadFile(){

    }

    return (
        <IonPage>
            <Header></Header>
            <IonContent scrollY={false} color="light" className="top-content" scrollEvents={true}>
            <IonContent color="light" className="left-content">
                {/*<Canvas>*/}
                {/*    <ambientLight intensity={0.5}/>*/}
                {/*    <spotLight position={[10, 15, 10]} angle={0.3}/>*/}
                {/*        <Model/>*/}
                {/*    <OrbitControls/>*/}
                {/*</Canvas>*/}
                <IonButton color="medium" shape="round" onClick={() => {downloadFile();}}>Download your model</IonButton>
                <IonContent>
                    <IonText><h3>What now?</h3></IonText>
                    <IonText><p>Load your downloaded file in your favourite OBJ viewer. Don't have one? Use </p> <a href="https://3dviewer.net/" target="_blank">Online 3D Viewer</a></IonText>
                </IonContent>

            </IonContent>
            <IonContent className="right-content">
                <IonButton color="medium" shape="round" onClick={() => {getShareLink()}}>Get link to model</IonButton>
                <IonCard>
                    <IonCardTitle><h5>My notes:</h5></IonCardTitle>
                    <IonCardContent>
                        <IonTextarea className="text"></IonTextarea>
                        <IonButton color="medium" shape="round">Save notes</IonButton>
                    </IonCardContent>
                </IonCard>
            </IonContent>
            </IonContent>
            <IonContent className="bottom-content">
                <IonCard>
                    <IonCardTitle><h5>Comments:</h5></IonCardTitle>
                    <IonCardContent>
                        <IonList>

                        </IonList>
                    </IonCardContent>
                </IonCard>
            </IonContent>
            <Footer></Footer>
        </IonPage>
    )
}
