import React from "react";
import {IonCardContent, IonCardTitle, IonItem} from "@ionic/react";
import './ScansHome.css';
import {CommentProps} from "./CommentProps";


const Comment: React.FC<CommentProps> = ({id, username, scanid, text, date}) => {

    return (
        <IonItem className="item">
            <IonCardContent>
                <h5>{date}</h5>
                <IonCardContent>{text}</IonCardContent>
                <h5>by {username}</h5>
            </IonCardContent>
        </IonItem>
    )
}

export default Comment;