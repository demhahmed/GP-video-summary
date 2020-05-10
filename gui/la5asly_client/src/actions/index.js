import {
  ERROR,
  SIGN_IN,
  SIGN_OUT,
  SUMMARIZE,
  SHOW_NOTIFICATION,
  HIDE_NOTIFICATION,
  FETCH_SUMMARIES,
} from "./types";

import axios from "../apis";

export const signIn = (userId, username, image) => async (dispatch) => {
  try {
    dispatch({ type: SIGN_IN, payload: { userId, username, image } });
    showPopUp(`Welcome ${username} to La5asly`, dispatch);
  } catch (error) {
    handleError(error, dispatch);
  }
};

export const signOut = () => async (dispatch) => {
  try {
    dispatch({ type: SIGN_OUT });
  } catch (error) {
    handleError(error, dispatch);
  }
};

export const fetchSummaries = (filterObject) => async (dispatch) => {
  // Example of filter object { username: "Moamen", leagueType: "PREMIER_LEAGUE" }
  try {
    let response = await axios.get("/fetch_summaries", {
      params: filterObject,
    });
    dispatch({ type: FETCH_SUMMARIES, payload: response.data });
  } catch (error) {
    handleError(error, dispatch);
  }
};

export const summarize = (userId, leagueType, file) => async (dispatch) => {
  // Example of filter object { username: "Moamen", leagueType: "PREMIER_LEAGUE" }
  try {
    const formData = new FormData();
    formData.append("video", file);
    await axios.post("/summarize", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
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
    type: SHOW_NOTIFICATION,
    payload: message,
  };
};

export const hideNotification = () => {
  return {
    type: HIDE_NOTIFICATION,
  };
};


function showPopUp(message, dispatch) {
  dispatch({ type: SHOW_NOTIFICATION, payload: message });
  setTimeout(() => {
    dispatch({ type: HIDE_NOTIFICATION });
  }, 2000);
}

function handleError(error, dispatch) {
  showPopUp("Error Occured", dispatch);
}
