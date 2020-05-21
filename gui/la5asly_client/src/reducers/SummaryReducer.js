import { FETCH_SUMMARIES, ADD_SUMMARY } from "../actions/types";

export default (state = [], action) => {
  switch (action.type) {
    case FETCH_SUMMARIES:
      return action.payload;
    case ADD_SUMMARY:
      return [...state, action.payload];
    default:
      return state;
  }
};
