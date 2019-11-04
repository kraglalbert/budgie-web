import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
// import axios from 'axios'

// import example from './module-example'

Vue.use(Vuex)

// var config = require('../config')

// // Axios config
// const frontendUrl = 'http://' + config.build.host + ':' + config.build.port
// const backendUrl =
//   'http://' + config.build.backendHost + ':' + config.build.backendPort

// var AXIOS = axios.create({
//   baseURL: backendUrl,
//   headers: { 'Access-Control-Allow-Origin': frontendUrl, 'Content-Type': 'application/json' }
// })

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    state: {
      currentUser: {
        name: String,
        email: String
      }
    },
    getters: {},
    mutations: {
      login (state, { name, email }) {
        state.currentUser.name = name
        state.currentUser.email = email
      },
      logout (state) {
        state.currentUser = null
      }
    },
    actions: {},
    modules: {
      // example
    },
    plugins: [createPersistedState()],

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  })

  return Store
}
