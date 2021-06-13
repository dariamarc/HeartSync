import React, { useContext} from "react";
import { Redirect, Route } from "react-router-dom";
import { getLogger } from "../shared";
import { AuthState, AuthContext } from "./AuthProvider";
import PropTypes from 'prop-types';

const log = getLogger('Login');

export interface PrivateRouteProps {
    component: PropTypes.ReactNodeLike;
    path: string;
    exact?: boolean;
}

export const PrivateRoute: React.FC<PrivateRouteProps> = ({ component: Component, ...rest }) => {
    const { isAuthenticated, token } = useContext<AuthState>(AuthContext);
    log('render, isAuthenticated', isAuthenticated);
    return (
        <Route {...rest} render={props => {
            if (isAuthenticated) {
                // @ts-ignore
                return <Component {...props} />;
            }
            else {
                return <Redirect to={{ pathname: '/welcome' }}/>
            }
        }}/>
    );
}