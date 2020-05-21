import { FETCH_TEAMS } from "../actions/types";
import _ from "lodash";

const initialState = {
  teams: null,
  leagues: null,
};

export default (state = initialState, action) => {
  switch (action.type) {
    case FETCH_TEAMS:
      const leagues = action.payload.map((team) => ({
        name: team.league.name,
        logo: team.league.logo,
        _id: team.league._id,
      }));
      return {
        teams: action.payload,
        leagues: _.uniqBy(leagues, "_id"),
      };
    default:
      return state;
  }
};
