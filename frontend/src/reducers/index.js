import {combineReducers} from "redux";
import {reducer as formReducer} from "redux-form";

import {accountReducer,} from "./account";
import {clientsReducer} from "./clients";
import {serversReducer} from "./servers";
import {settingsReducer} from "./settings";

const rootReducer = combineReducers({
    clients: clientsReducer,
    servers: serversReducer,
    account: accountReducer,
    settings: settingsReducer,
    form: formReducer
});

export default rootReducer;
