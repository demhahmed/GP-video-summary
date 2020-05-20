import { combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";
import NotificationReducer from "./NotificationReducer";
import SummaryReducer from "./SummaryReducer";
import UserReducer from "./UserReducer";
import TeamReducers from "./TeamReducers";

export default combineReducers({
  form: formReducer,
  notifications: NotificationReducer,
  user: UserReducer,
  summaries: SummaryReducer,
  teams: TeamReducers
});
