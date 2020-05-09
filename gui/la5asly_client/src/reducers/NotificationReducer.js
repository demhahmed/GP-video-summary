import {SHOW_NOTIFICATION, HIDE_NOTIFICATION} from "../actions/types";

// Default state
const notifyDefault = {
    display: false,
    message: ''
};

export default (state = notifyDefault, action) => {
    switch (action.type) {
        case SHOW_NOTIFICATION:
            return {
                display: true,
                message: action.payload
            };
        case HIDE_NOTIFICATION:
            return {
                display: false,
                message: "  "
            };
        default:
            return state;
    }
};