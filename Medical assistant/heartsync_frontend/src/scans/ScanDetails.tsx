import React, {useRef} from "react";
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
    IonLabel,
    IonPage
} from "@ionic/react";

interface ScanDetailsProps extends RouteComponentProps<{
    _scanId?: string
}>{}

export const ScanDetails: React.FC<ScanDetailsProps> = ({history, match}) => {


    // function Box()  {
    //     return (
    //         <mesh>
    //             <boxBufferGeometry attach="geometry"></boxBufferGeometry>
    //             <meshLambertMaterial attach="material" color="red"></meshLambertMaterial>
    //         </mesh>
    //     );
    // }


    return (
        <IonPage>
            <Header></Header>
            <IonContent color="light" className="left-content">
                {/*<Canvas>*/}
                {/*    <ambientLight intensity={0.5}/>*/}
                {/*    <spotLight position={[10, 15, 10]} angle={0.3}/>*/}
                {/*    <Box/>*/}
                {/*</Canvas>*/}
            </IonContent>
            <IonContent className="right-content"></IonContent>
            <Footer></Footer>
        </IonPage>
    )
}