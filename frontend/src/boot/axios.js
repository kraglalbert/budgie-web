import Vue from 'vue'
import axios from 'axios'

var config = require('../config')

// Axios config
const frontendUrl = 'http://' + config.build.host + ':' + config.build.port
const backendUrl =
  'http://' + config.build.backendHost + ':' + config.build.backendPort

Vue.prototype.$axios = axios.create({
  baseURL: backendUrl,
  headers: { 'Access-Control-Allow-Origin': frontendUrl, 'Content-Type': 'application/json' }
})
