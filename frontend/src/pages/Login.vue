<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex column flex-center">
        <div
          class="q-gutter-y-md"
          style="min-width: 300px"
        >
          <q-card>
            <q-tabs
              v-model="tab"
              dense
              class="text-grey"
              active-color="primary"
              indicator-color="primary"
              align="justify"
              narrow-indicator
            >
              <q-tab
                name="login"
                label="Log In"
              />
              <q-tab
                name="signup"
                label="Sign Up"
              />
            </q-tabs>

            <q-separator />

            <q-tab-panels
              v-model="tab"
              animated
            >
              <q-tab-panel name="login">
                <q-form
                  @submit="onLogIn"
                  class="q-gutter-md"
                >
                  <q-input
                    filled
                    v-model="email"
                    label="Email"
                    hint="Enter your email"
                    lazy-rules
                    :rules="[ val => val && val.length > 0 || 'Please enter your email']"
                  />

                  <q-input
                    filled
                    v-model="password"
                    label="Password"
                    type="password"
                    hint="Enter your password"
                    lazy-rules
                    :rules="[ val => val !== null && val !== '' || 'Please type your password']"
                  />

                  <div>
                    <q-btn
                      label="Log In"
                      type="submit"
                      color="primary"
                    />
                  </div>
                </q-form>
              </q-tab-panel>

              <q-tab-panel name="signup">
                <q-form
                  @submit="onSignUp"
                  class="q-gutter-md"
                >
                  <q-input
                    filled
                    v-model="name"
                    label="Name"
                    hint="Enter your name"
                    lazy-rules
                    :rules="[ val => val && val.length > 0 || 'Please enter your name']"
                  />

                  <q-input
                    filled
                    v-model="email"
                    label="Email"
                    hint="Enter your email"
                    lazy-rules
                    :rules="[ val => val && val.length > 0 || 'Please enter your email']"
                  />

                  <q-input
                    filled
                    v-model="password"
                    label="Password"
                    type="password"
                    hint="Enter your password"
                    lazy-rules
                    :rules="[ val => val !== null && val !== '' || 'Please type your password']"
                  />

                  <q-input
                    filled
                    v-model="confirm_password"
                    label="Confirm Password"
                    type="password"
                    hint="Confirm your password"
                    lazy-rules
                    :rules="[
                        val => val !== null && val !== '' || 'Please confirm your password',
                        val => val === password || 'Passwords do not match'
                    ]"
                  />

                  <div>
                    <q-btn
                      label="Sign Up"
                      type="submit"
                      color="primary"
                    />
                  </div>
                </q-form>
              </q-tab-panel>
            </q-tab-panels>
          </q-card>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import axios from 'axios'
var config = require('../config')

// Axios config
const frontendUrl = 'http://' + config.build.host + ':' + config.build.port
const backendUrl =
  'http://' + config.build.backendHost + ':' + config.build.backendPort

var AXIOS = axios.create({
  baseURL: backendUrl,
  headers: { 'Access-Control-Allow-Origin': frontendUrl, 'Content-Type': 'application/json' }
})

export default {
  name: 'Login',

  data () {
    return {
      name: null,
      email: null,
      password: null,
      confirm_password: null,

      tab: 'login'
    }
  },

  methods: {
    onLogIn () {
      AXIOS.post('/account/login', { email: this.email, password: this.password })
        .then(res => {
          if (res.status === 200) {
            this.$q.notify({
              color: 'green-4',
              position: 'top',
              textColor: 'white',
              icon: 'cloud_done',
              message: 'Logged In'
            })
          }
        }).catch(_err => {
          this.$q.notify({
            color: 'red-4',
            position: 'top',
            textColor: 'white',
            icon: 'error',
            message: 'Wrong email or password'
          })
        })
    },
    onSignUp () {
      AXIOS.post('/account/register', {
        name: this.name, email: this.email, password: this.password
      }).then(res => {
        if (res.status === 200) {
          this.$q.notify({
            color: 'green-4',
            position: 'top',
            textColor: 'white',
            icon: 'cloud_done',
            message: 'Signed Up Successfully'
          })
        }
      }).catch(_err => {
        this.$q.notify({
          color: 'red-4',
          position: 'top',
          textColor: 'white',
          icon: 'error',
          message: 'Sign Up Error'
        })
      })
    }
  }
}
</script>
