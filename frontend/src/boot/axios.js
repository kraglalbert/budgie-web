import Vue from "vue";
import axios from "axios";
import Store from "../store";
import Router from "../router";

var config = require("../config");

// Axios config
const frontendUrl = config.build.host + ":" + config.build.port;
const backendUrl = config.build.backendHost + ":" + config.build.backendPort;

const AXIOS = axios.create({
  baseURL: backendUrl,
  headers: {
    "Access-Control-Allow-Origin": frontendUrl,
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

// set up interceptor to handle expired access tokens
AXIOS.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (Store.getters.isLoggedIn) {
      if (error.response.status === 401) {
        // get user with stored token
        AXIOS.post("/auth/token/refresh", null, {
          headers: {
            "X-CSRF-TOKEN": Cookies.get("csrf_refresh_token"),
          },
        })
          .then((resp) => {
            Store.commit("set_user", resp.data.user);
          })
          .catch(() => {
            // token is invalid
            Store.dispatch("logout").then(Router.push({ path: "/login" }));
          });
      } else {
        Router.push({ path: "/login" });
      }
    } else {
      return Promise.reject(error);
    }
  }
);

Vue.prototype.$axios = AXIOS;
