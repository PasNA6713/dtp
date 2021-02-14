<template>
  <div id="container"> 
    <v-card height="600px" width="600px">
      <div>
        <p style="
        font-family: Century Gothic;
        font-style: normal;
        font-weight: bold;
        font-size: 35px;
        line-height: 43px;
        text-align: center;
        color: #27646A;
        text-transform: uppercase;">Авторизация</p>

        <v-text-field
          v-model="username"
          label="Имя пользователя"
          type="name"
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="Пароль"
          type="password"
          required
        ></v-text-field>

        <v-btn
          :disabled="!valid"
          color="#27646A"
          @click="signin"
          class="mt-3 but"
          block
          large
        >
          Войти
        </v-btn>

        <router-link :to="{name: 'signup'}" class="no-link-decoration">
        <v-btn
          :disabled="!valid"
          color="#F58D8E"
          class="mt-3 but"
          block
          large
        >
          Зарегистрироваться
        </v-btn>
        </router-link>

      </div>

      <v-row justify="space-around"  class="d-flex align-items-center" style="
      width: 300px;
      margin: 20px auto 20px;">
        <v-btn
            fab
            dark
            style="width: 36px; height: 36px"
            elevation="0"
            color="#27646A"
          >
          <v-icon dark>mdi-google</v-icon>
        </v-btn>

        <v-icon
          x-large
          color="#27646A"
        >mdi-facebook</v-icon>

        <v-icon
          x-large
          color="#27646A"
        >mdi-vk</v-icon>
      </v-row>
    </v-card>
  </div> 
</template>

<script>

  export default {
    name: 'SignIn',

    data: () => ({
      valid: true,
      password: null,
      username: null,
      logged: false
    }),

    methods: {
      signin() {
        let headers = {
                    'Content-Type': 'application/json'
                }
        let body = JSON.stringify({
                    username: this.username,
                    password: this.password
                })

          axios.post(`${this.$store.state.backendUrl}/auth/token/login/`, body, {headers}
          ).then(response => {
              const token = response.data.auth_token
              this.$store.commit('setToken', token);
              console.log(token)
              this.$router.push('/map')
              })
      }
    },

    created: function(){
      if (this.$store.state.token) {
        this.logged = true 
        console.log("Logged!")
      }
      else {
        console.log("Unauthorized!")
      }
    }
  }

</script>

<style scoped>
.but {
  font-family: Century Gothic;
  font-style: normal;
  font-weight: bold;
  font-size: 15px;
  line-height: 43px;
  text-align: center;
  color: white;
  text-transform: uppercase;
}

.v-card {
  margin: auto;
  margin-top: 170px;
  height: 600px;
  width: 600px;
  padding: 30px;
}

.no-link-decoration {
  text-decoration: none; 
  color:black;
}

#container {
    background-image: url(../../assets/img/IMG_461.png);
    background-size: cover;
    height: 100%;
  }
</style>
