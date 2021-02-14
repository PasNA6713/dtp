<template>
  <div id="stat">
    <h1>Статистика</h1>
  </div>
</template>

<script>
export default {
  name: 'statistics',
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
