import {combineReducers} from 'redux';
import {reducer as formReducer} from 'redux-form';
import NotificationReducer from "./NotificationReducer";

export default combineReducers({
    form: formReducer,
    notifications: NotificationReducer
});
