<template>
  <div id="about">
    <Navbar/>
    <v-img
      id="image-about"
      height="80%"
      width="80%"
      src="../../assets/img/about_project.png">
    </v-img>
    
    <div class="img-wrap">
      <img
        id="image-rectangle"
        height="50%"
        width="20%"
        src="../../assets/img/Rectangle 5.png"/>
      <h1 class="title">О проекте</h1>
    </div>
    <p class="maintext">Существует целый ряд методик по предотвращению дорожно-транспортных</p>
    <p class="maintext">правонарушений, начиная от профилактических бесед с водителями и заканчивая</p>
    <p class="maintext">системой штрафов и другими видами административной ответственности.</p>
    <p class="maintext">Наша страна довольно специфична, и увы, законы и метод убеждения не всегда работают так, как</p>
    <p class="maintext">нам хочется. Именно поэтому мы решили создать нечто, позволяющее если не в корень,</p>
    <p class="maintext">то под основание решить проблему. Мы перешли к действиям</p>
    <p class="maintext">В основе нашего продукта лежит анализ всех ДТП с целью составления полной картины</p>
    <p class="maintext">происшествий, четкая структуризация и визуализация аварий, что очень удобно для</p>
    <p class="maintext">понимания обстановки руководителей муниципалитетов и непосредственных</p>
    <p class="maintext">исполнителей. Как итог, мы создали простую понятную инструкцию, как эффективно</p>
    <p class="maintext">использовать человеческий потенциал, руководствуясь драгоценностью времени</p>
    <p class="maintext">каждого из нас</p>
    <p class="maintext">В нашем проекте мы собрали данные обо всех авариях за последние 10 лет, за это</p>
    <p class="maintext">спасибо, они ведут полную статистику и позволяют нам ее видеть. В результате мы</p>
    <p class="maintext">получили сервис, который анализирует базу данных с авариями, выявляет наиболее</p>
    <p class="maintext">слабые места в дорожной карте, и предлагает максимально эффективное</p>
    <p class="maintext">расставление патрулей ДПС в городе. Также хочется подчеркнуть, сервис обладает динамическим</p>
    <p class="maintext">чем-то, и в зависимости от количества патрулей, соответственно рекомендовать</p>
    <p class="maintext">руководителям наиболее важные участки дорог, которым необходим</p>
    <p class="maintext">дополнительный контроль.</p> 
  </div>
</template>

<script>
  import Navbar from '../Navbar.vue'

  export default {
    name: 'about-project',

    components: {
      Navbar
    },

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
  #image-about {
    display: block;
    margin: auto;
  }

  #image-rectangle {
    top: -30px;
    left: 190px;
    position: relative;
  }

  .title {
    font-family: Open Sans;
    font-style: normal;
    font-weight: 900;
    font-size: 100px;
    line-height: 50px;
    color: white;
  }

  .img-wrap h1 {
    position: absolute;
    left: 250px;
    bottom: 1035px;
    width: 100%;
  }

  .maintext {
    margin-left: 190px;
    font-family: Roboto;
    font-size: 20px;
    font-style: normal;
    font-weight: 400;
    line-height: 30px;
    letter-spacing: 0em;
    }

</style>