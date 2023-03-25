import { SET_CURRENT_USER, USER_LOADING } from "../actions/types";

const isEmpty = require("is-empty");

const initialState = {
  isAuthenticated: false,
  user: {},
  loading: false
};

export default function authReducer(state = initialState, action) {
/* A switch statement that is checking the action type. If the action type is SET_CURRENT_USER, it will
return the state with the isAuthenticated and user properties set to the payload. If the action type
is USER_LOADING, it will return the state with the loading property set to true. If the action type
is neither of these, it will return the state. */
  switch (action.type) {
    case SET_CURRENT_USER:
      return {
        ...state,
        isAuthenticated: !isEmpty(action.payload),
        user: action.payload
      };
    case USER_LOADING:
      return {
        ...state,
        loading: true
      };
    default:
      return state;
  }
}