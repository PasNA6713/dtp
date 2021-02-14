<template>
<div id="gradient">  
  <v-row 
    justify="center"
    id="navbar">
      <v-col cols=2>
        <h1 id="safety-map">Safety Map</h1>
      </v-col>
      <v-col cols=3
      class="text-center">
        <router-link :to="{name: 'about-project'}" class="no-link-decoration nav-buttons">О проекте</router-link>
      </v-col>
      <v-col cols=3
      class="text-center"> 
        <router-link :to="{name: 'statistics'}" class="no-link-decoration nav-buttons">Статистика</router-link>
      </v-col>
      <v-col cols=3
      class="text-center">
        <router-link :to="{name: 'map'}" class="no-link-decoration nav-buttons">Карта</router-link>
      </v-col>
      <v-col cols=1 
      class="text-center">
        <v-icon
          large
          color="white"
          v-if="logged"
          aria-hidden="false"
        >
          mdi-account
        </v-icon>
        <router-link :to="{name: 'signin'}" class="no-link-decoration nav-buttons" v-if="!logged">
          <v-icon
            large
            color="white"
            aria-hidden="false"
          >
            mdi-account-off
          </v-icon>
        </router-link>
      </v-col>     
  </v-row>
  </div>
</template>

<style scoped>
  #safety-map {
    font-family: Montserrat;
    font-size: 35px;
    font-style: normal;
    font-weight: 600;
    line-height: 30px;
    letter-spacing: 0em;
    text-align: center;
    color: #FFFFFF;
    opacity: 50%;
  }

  .nav-buttons {
    font-family: Montserrat;
    font-size: 25px;
    font-style: normal;
    font-weight: 600;
    line-height: 30px;
    letter-spacing: 0em;
    text-align: left;
  }

  #navbar {
    padding-top: 50px;
    padding-left: 250px;
    padding-bottom: 85px;
  }

  .no-link-decoration {
    text-decoration: none;
    color: white;
  } 

  .nav-buttons:after {
    display: block;
    left: 0; 
    width: 0;
    height: 2px; 
    background-color: #FFFFFF; 
    content: "";
    transition: width 0.3s ease-out; 
}

  .nav-buttons:hover:after,
  .nav-buttons:focus:after {
    width: 100%; 
  }
</style>

<script>
  export default {
    name: 'Navbar',
    data: () => ({
      logged: false
    }),

    created: function(){
      if (this.$store.state.token) {
        this.logged = true 
        console.log("Logged!")
      }
    }
  }
</script>

