import {
    SIGN_IN,
    SIGN_UP,
    SIGN_OUT, RESERVE_MOVIE_SCREEN
} from '../actions/types';

const initialState = {
    user: null
};

export default (state = initialState, action) => {
    switch (action.type) {
        case SIGN_IN:
            return {...state, user: action.payload};
        case SIGN_OUT:
            return {...state, user: null};
        default:
            return state;
    }
};