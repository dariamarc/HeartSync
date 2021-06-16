import { Redirect, Route } from 'react-router-dom';
import { IonApp, IonRouterOutlet } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

/* Theme variables */
import './theme/variables.css';
import {Welcome} from "./welcome/Welcome";
import React from "react";
import {Login} from "./auth/Login";
import {Signup} from "./auth/Signup";
import {ScansHome} from "./scans/ScansHome";
import {AuthProvider} from "./auth/AuthProvider";
import {PrivateRoute} from "./auth/PrivateRoute";
import {ScanProvider} from "./scans/ScanProvider";
import {ScanDetails} from "./scans/ScanDetails";
import {CommentProvider} from "./comments/CommentProvider";
import {FileProvider} from "./file/FileProvider";
import {NoteProvider} from "./notes/NoteProvider";
import {About} from "./welcome/About";

const App: React.FC = () => (

  <IonApp>
    <IonReactRouter>
      <IonRouterOutlet>
        <AuthProvider>
          <ScanProvider>
            <CommentProvider>
              <FileProvider>
                <NoteProvider>
        <Route exact path="/welcome" component={Welcome}/>
                    <Route exact path="/about" component={About}/>
          <Route exact path="/login" component={Login}/>
          <Route exact path="/signup" component={Signup}/>
          <PrivateRoute exact path="/home" component={ScansHome}/>
          <PrivateRoute exact path="/scan/:_scanId" component={ScanDetails}/>
        <Route exact path="/">
          <Redirect to="/welcome" />
        </Route>
                </NoteProvider>
              </FileProvider>
            </CommentProvider>
          </ScanProvider>
        </AuthProvider>
      </IonRouterOutlet>
    </IonReactRouter>
  </IonApp>
);

export default App;
