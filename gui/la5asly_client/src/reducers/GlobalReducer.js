import { CANCEL_WAIT_FETCH, WAIT_FETCH } from "../actions/types";

const globalReducer = {
  wait: false,
};

export default (state = globalReducer, action) => {
  switch (action.type) {
    case WAIT_FETCH:
      return {
        wait: true,
      };
    case CANCEL_WAIT_FETCH:
      return {
        wait: false,
      };
    default:
      return state;
  }
};
