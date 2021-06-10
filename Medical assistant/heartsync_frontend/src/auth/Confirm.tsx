import React, {useContext, useEffect} from "react";
import {RouteComponentProps} from "react-router";
import {IonPage} from "@ionic/react";
import {ConfirmEmailContext} from "./AuthProvider";
import {Header} from "../layout/Header";
import {Footer} from "../layout/Footer";
import './Confirm.css';

interface ConfirmDetailsProps extends RouteComponentProps<{
    _emailToken?: string
}>{

}

export const Confirm: React.FC<ConfirmDetailsProps> = ({history, match}) => {
    const {isConfirmed, isConfirming, confirmEmail, confirmEmailError} = useContext(ConfirmEmailContext);

    useEffect(() => {
        const emailToken = match.params._emailToken || '';
        confirmEmail?.(emailToken);
    }, [match.params._emailToken])
    return (
        <IonPage>
            <Header></Header>
            {isConfirmed &&
            <div className="center"><h3>Your email address is confirmed, you can sing in.</h3></div>}
            {confirmEmailError &&
            <div className="center"><h3>Something went wrong, could not confirm your email.</h3></div>}
            <Footer></Footer>
        </IonPage>
    )
}