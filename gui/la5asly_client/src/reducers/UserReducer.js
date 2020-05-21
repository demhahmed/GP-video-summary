import { FETCH_USER, LOG_OUT, FETCH_USER_IMAGE } from "../actions/types";
import _ from "lodash";

const initialState = {
  isLoggedIn: false,
};

export default (state = initialState, action) => {
  switch (action.type) {
    case FETCH_USER:
      return { isLoggedIn: true, ...action.payload };
    case FETCH_USER_IMAGE:
      return { ...state, image_loaded: action.payload };
    case LOG_OUT:
      return { isLoggedIn: false };
    default:
      return state;
  }
};
