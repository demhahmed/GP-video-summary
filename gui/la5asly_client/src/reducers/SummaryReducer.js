import { FETCH_SUMMARIES } from "../actions/types";

import _ from "lodash";

const initialState = {
    summaries: [],
};

export default (state = initialState, action) => {
    switch (action.type) {
        case FETCH_SUMMARIES:
            return { ...state, summaries: _.cloneDeep(action.payload) };
        default:
            return state;
    }
};
