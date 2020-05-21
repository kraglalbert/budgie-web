import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

// import example from './module-example'

Vue.use(Vuex);

var config = require("../config");

// Axios config
const frontendUrl = config.build.host + ":" + config.build.port;
const backendUrl = config.build.backendHost + ":" + config.build.backendPort;

var AXIOS = axios.create({
  baseURL: backendUrl,
  headers: {
    "Access-Control-Allow-Origin": frontendUrl,
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

const Store = new Vuex.Store({
  state: {
    status: "",
    currentUser: null,
  },
  getters: {
    userExists: (state) => state.currentUser !== null,
    authStatus: (state) => state.status,
    userCurrency: (state) => state.currentUser.default_currency,
  },
  mutations: {
    auth_request(state) {
      state.status = "loading";
    },
    auth_success(state, authObj) {
      state.status = "success";
      state.currentUser = authObj.user;
      state.userExists = true;
    },
    auth_error(state) {
      state.status = "error";
    },
    logout(state) {
      state.status = "";
      state.token = "";
      state.currentUser = null;
      state.userExists = false;
    },
    set_user(state, user) {
      state.currentUser = user;
      state.userExists = true;
    },
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit("auth_request");
        AXIOS.post("/auth/login", {
          email: user.email,
          password: user.password,
        })
          .then((resp) => {
            const user = resp.data.user;

            commit("auth_success", { user });
            resolve(resp);
          })
          .catch((err) => {
            commit("auth_error");
            reject(err);
          });
      });
    },
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit("auth_request");
        AXIOS.post("/auth/register", {
          name: user.name,
          email: user.email,
          password: user.password,
        })
          .then((resp) => {
            const user = resp.data.user;

            commit("auth_success", { user });
            resolve(resp);
          })
          .catch((err) => {
            commit("auth_error", err);
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        commit("logout");
        resolve();
      });
    },
  },
  modules: {
    // example
  },

  // enable strict mode (adds overhead!)
  // for dev mode only
  strict: process.env.DEV,
});

export default Store;
