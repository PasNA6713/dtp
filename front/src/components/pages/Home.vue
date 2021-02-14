<template>
  <div id="container">    
    <Navbar />
    <v-row
      align="center"
      justify="center"
      >
        <v-col
          class="text-center"
          cols="12"
          id=title
        >
          <h1>
            Анализатор дорожно-транспортных 
          </h1>
          <h1 class="subheading">
            происшествий
          </h1>
        </v-col>
    </v-row>

    <v-row
      align="center"
      justify="center"
      v-if="!logged">
      <v-btn
        id="button_login"
        >
        <router-link :to="{name: 'signin'}" class="no-link-decoration">Войти в аккаунт</router-link>
      </v-btn>
    </v-row>

    <v-row id="signed-in" v-else>
    </v-row>

    <div id="gradient2">
      <v-row
      align="center"
      justify="center">
        <h1 class="bottom-title">Почему мы?</h1>   
      </v-row>

      <v-row>
        <v-col cols=4>
          <h1 class="bottom-title2">Скорость</h1>  
        </v-col> 
        <v-col cols=4>
          <h1 class="bottom-title2">Точность</h1>  
        </v-col>
        <v-col cols=4>
          <h1 class="bottom-title2">Значимость</h1>  
        </v-col> 
      </v-row>

      <v-row>
        <v-col cols=4>
          <img src="../../assets/img/rocket.svg" height="70" width="70" alt="rocket" class="bottom-svg"/>
        </v-col>
        <v-col cols=4>
          <img src="../../assets/img/clock.svg" height="70" width="70" alt="clock" class="bottom-svg"/>
        </v-col>
        <v-col cols=4>
          <img src="../../assets/img/build.svg" height="70" width="70" alt="build" class="bottom-svg"/>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols=4>
          <p class="bottom-text">
            Мы предлагаем детальный разбор
          </p>
          <p class="bottom-text">всех ДТП и путей решений в формате</p>
          <p class="bottom-text">онлайн</p>
        </v-col> 
        <v-col cols=4>
          <p class="bottom-text">Разработаная метаматическая модель</p>
          <p class="bottom-text">позволяет максимально точно находить слабые места в городе,</p> 
          <p class="bottom-text">что не под силу делать людям вручную</p>  
        </v-col>
        <v-col cols=4>
          <p class="bottom-text">Безопасность - основа социального</p>
          <p class="bottom-text">благополучия граждан и важный фактор</p> 
          <p class="bottom-text">в оценке деятельности органов управления</p>  
        </v-col> 
      </v-row>
    </div>
  </div>
</template>

<script>
import Navbar from '../Navbar.vue'

export default {
  components: { Navbar },
  name: 'home',

  data: () => ({
    logged: false
  }),

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
  h1 {
    color: #FFFFFF;
    font-size: 40px;
    font-style: normal;
    font-weight: 800;
    line-height: 54px;
    letter-spacing: 0em;
    text-align: center;
  }

  #container {
    background-image: url(../../assets/img/IMG_4461.png);
    background-size: cover;
    height: 100%;
  }

  #gradient {
    background: linear-gradient(90deg, rgba(54, 61, 83, 0.6) 0%, rgba(70, 66, 62, 0.6) 26.28%, rgba(111, 62, 0, 0.462) 60.05%, rgba(54, 61, 83, 0.6) 100%);
  }

  #gradient2 {
    background: rgba(231, 231, 231, 0.3);
  }

  #title {
    justify-content: center;
    padding-top: 200px;
  }

  #button_login {
    width: 231px;
    height: 42px;

    font-family: Open Sans;
    font-style: normal;
    font-weight: 600;
    font-size: 18px;
    line-height: 25px;
    text-align: center;

    color: #C6C6C6;

    background: #212F3C;
    border-radius: 15px;

    margin-top: 50px;
    margin-bottom: 155px;
  }

  #signed-in {
    margin-bottom: 245px;
  }

  .bottom-title {
    font-family: Open Sans;
    font-size: 21px;
    font-style: normal;
    font-weight: 700;
    line-height: 29px;
    letter-spacing: 0.02em;
    text-align: center;
    margin-top: 20px;
  }

  .bottom-title2 {
    font-family: Open Sans;
    font-size: 18px;
    font-style: normal;
    font-weight: 400;
    line-height: 25px;
    letter-spacing: 0em;
    text-align: center;
  }

  .bottom-svg {
    margin-left: 310px;
  }

  .bottom-text {
    font-family: Open Sans;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 19px;
    letter-spacing: 0em;
    text-align: center;
    color: #FFFFFF;
  }

  .no-link-decoration {
    text-decoration: none;
    color: white;
  } 
</style>

