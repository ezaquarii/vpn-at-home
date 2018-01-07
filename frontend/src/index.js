import "babel-polyfill";
import "semantic-ui-css/semantic.min.css";
import "./css/styles.css";

import React from "react";
import {composeWithDevTools} from "redux-devtools-extension";
import ReactDOM from "react-dom";
import {Provider} from "react-redux";
import {BrowserRouter, Route} from "react-router-dom";

import {createStore, applyMiddleware} from "redux";
import ReduxPromise from "redux-promise";
import thunk from "redux-thunk";

import reducers from "./reducers";
import {App} from "./components/app";

const createStoreWithMiddleware = composeWithDevTools(applyMiddleware(ReduxPromise, thunk))(createStore);

function rootComponent() {
    return(
        <div className={"full-height"}>
            <BrowserRouter>
                <Provider store={createStoreWithMiddleware(reducers)}>
                    <Route path='/' component={App}/>
                </Provider>
            </BrowserRouter>
        </div>
    );
}

ReactDOM.render(
    rootComponent()
    , document.querySelector("#root"));
