<template>
  <div>
    <Navbar/>
    <router-view/>
    <Footer/>
  </div>
</template>

<script>
  import Navbar from "../components/Navbar.vue";
  import Footer from "../components/Footer.vue";

  export default {
    name: 'Main',

    components: {
        Navbar,
        Footer
    }
  };
</script>

<style scoped>
  #gradient {
      background-color: #212F3C;
    }
</style>