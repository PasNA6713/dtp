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
          text-transform: uppercase;">Регистрация</p>

          <v-text-field
          v-model="mail"
          label="Почтовый ящик"
          type="email"
          required
          ></v-text-field>

          <v-text-field
          v-model="username"
          label="Имя"
          type="text"
          required
          ></v-text-field>

          <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              required
          ></v-text-field>

          <v-btn
              color="#F58D8E"
              @click="signUp"
              class="mt-3 but"
              block
              large
          >
              Зарегистрироваться
          </v-btn>

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
    name: 'SignUp',

    data: () => ({
      password: null,
      confirm_password: null,
      mail: null,
      username: null,
      isCreated: false,
      error: [],
      logged: false
    }),
    methods: {
      signUp() {
        let headers = {
                  'Content-Type': 'application/json'
              }
        let body = JSON.stringify({
                  username: this.username,
                  password: this.password,
                  email: this.email
              })

        axios.post(`${this.$store.state.backendUrl}/auth/users/`, body, {headers}
        ).then(response => {
              if (response.username === this.firstname) {
                  this.$router.go(-1)
              }
              else {
                  this.isCreateFault = true
                  this.error = response
              }
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

#container {
    background-image: url(../../assets/img/IMG_461.png);
    background-size: cover;
    height: 100%;
  }
</style>
