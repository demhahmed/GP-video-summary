import * as types from "./types";
import axios from "axios";

export const fetchUser = () => async (dispatch) => {
  try {
    let response = await axios.get("/api/current_user");
    dispatch({ type: types.FETCH_USER, payload: response.data });
  } catch (error) {}
};

export const fetchSummaries = (filterObject) => async (dispatch) => {
  // Example of filter object { username: "Moamen", leagueType: "PREMIER_LEAGUE" }
  try {
    let response = await axios.get("/fetch_summaries", {
      params: { ...filterObject },
    });
    console.log(response.data);
    dispatch({ type: types.FETCH_SUMMARIES, payload: response.data });
  } catch (error) {
    handleError(error, dispatch);
  }
};

export const fetchTeams = () => async (dispatch) => {
  try {
    let response = await axios.get("/api/fetch_league_teams");
    dispatch({ type: types.FETCH_TEAMS, payload: response.data });
  } catch (error) {
    handleError(error, dispatch);
  }
};

export const summarize = (userId, title, leagueType, file, versions) => async (
  dispatch
) => {
  // Example of filter object { username: "Moamen", leagueType: "PREMIER_LEAGUE" }
  let versions_str = "";
  versions.forEach((version) => (versions_str += version + " "));
  versions_str = versions_str.trim();
  try {
    const formData = new FormData();
    formData.append("video", file[0]);
    await axios.post("/summarize", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      params: {
        user: userId,
        leagueType: leagueType.league,
        title,
        versions: versions_str,
      },
    });
    showPopUp(
      "File Uploaded Successfully and we're processing the video now",
      dispatch
    );
  } catch (error) {
    handleError(error, dispatch);
  }
};

export const showNotification = (message) => {
  return {
    type: types.SHOW_NOTIFICATION,
    payload: message,
  };
};

export const hideNotification = () => {
  return {
    type: types.HIDE_NOTIFICATION,
  };
};

function showPopUp(message, dispatch) {
  dispatch({ type: types.SHOW_NOTIFICATION, payload: message });
  setTimeout(() => {
    dispatch({ type: types.HIDE_NOTIFICATION });
  }, 2000);
}

function handleError(error, dispatch) {
  showPopUp(error.message, dispatch);
}
