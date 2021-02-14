<template>
  <div>
    <br>
    <v-container v-bind:class="{ isBigger: isAllDays }">
      <v-card>
        <v-row>
          <!-- Select Regions -->
          <v-col cols="3">
            <label for="region_filter">Регион:</label>
            <v-select
            id="region_filter"
            :items="regions"
            v-model="filterParams.region"
            :value="filterParams.region"
            placeholder="Пушкинский район"
            @change="changeMap"
            ></v-select>
          </v-col>

          <!-- Select Road Conditions -->
          <v-col cols="3">
            <label for="road_conditions_filter">Дорожные условия:</label>
            <v-select
            id="road_conditions_filter"
            :items="roadCondition"
            v-model="filterParams.roadCondition"
            :value="filterParams.roadCondition"
            placeholder="Отсутствие, плохая различимость горизонтальной разметки проезжей части"
            @change="changeMap"
          ></v-select>
          </v-col>

          <!-- Select Light -->
          <v-col cols="3">
            <label for="light_filter">Освещение</label>
            <v-select
            id="light_filter"
            :items="light"
            v-model="filterParams.light"
            @change="changeMap"
          ></v-select>
          </v-col>

          <!-- Input quontity of pattrols -->
          <v-col cols="3" v-if="logged" class="mt-6">
            <v-text-field 
            label="Рассчитать места концентрации"
            v-model="quontityPatrolls"
            :rules="rules"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <!-- Select Weather -->
          <v-col cols="3">
            <label for="weather_filter">Погода</label>
            <v-select
            id="weather_filter"
            :items="weather"
            v-model="filterParams.weather"
            :value="filterParams.weather"
            @change="changeMap"
            placeholder="Снегопад"
          ></v-select>
          </v-col>

          <!-- Select DTP's Category -->
          <v-col cols="3">
            <label for="category_filter">Тип ДТП:</label>
            <v-select
            id="category_filter"
            :items="category"
            v-model="filterParams.category"
            @change="changeMap"
          ></v-select>
            </v-col>

          <!-- Select location -->
            <v-col cols="3">
              <label for="location_filter">Место происшествия</label>
              <v-select
              id="location_filter"
              :items="location"
              v-model="filterParams.location"
              @change="changeMap"
            ></v-select>
            </v-col>

            <v-col cols="3" v-if="logged" class="mt-8">
              <v-btn
                elevation="2"
                @click="changeCameraMap"
              >Рассчитать места концентрации</v-btn>
            </v-col>
        </v-row>

        <v-row>
          <!-- Scroll time -->
          <v-slider
          :tick-labels="sliderTicks"
          :max="4"
          step="1"
          ticks="always"
          tick-size="3"
          v-model="filterParams.time"
          ></v-slider>
        </v-row>

        <!-- Select Day -->
        <v-row justify="center">
          <v-checkbox
            v-model="isAllDays"
            label="Все дни"
          ></v-checkbox>
          <v-date-picker
          v-if="!isAllDays"
          width="900px"
          :no-title="true"
          :show-current="false"
          v-model="filterParams.date"
          @change="changeMap"
          ></v-date-picker>
        </v-row>
      </v-card>
    </v-container>

      <v-spacer></v-spacer>
      <v-row>
        <v-col>
          <yandex-map  id="map"
              :settings="settings"
              :coords="mapCenter"
              :zoom="7" 
              :use-object-manager="true"
              :controls="['zoomControl']"
              @map-was-initialized="getMapInstance"
          >
          </yandex-map>
        </v-col>

        <v-col v-if="logged">
          <yandex-map  id="map2"
              :settings="settings"
              :coords="mapCenter"
              :zoom="7" 
              :use-object-manager="true"
              :controls="['zoomControl']"
              @map-was-initialized="getMapInstance2"
          >
          </yandex-map>
          <v-row class="two-buttons">
            <v-btn
            id="access-button" 
            @click="changeAccessToMap()"
            :disabled="isCurse"
            >
              Поставить точку
            </v-btn>
            <v-btn
            id="delete-button" 
            @click="deleteUserPoint()"
            :disabled="(isCurse && (user_placemark==null)) || isCurse || !user_placemark"
            >
              Удалить точку
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
      <br>
      <v-data-table
        :headers="tableHeaders"
        :items="accidentInfo"
        :search="tableSearch"
        group-by="Кластер"
        show-group-by
      >
      </v-data-table>
      <v-spacer></v-spacer>
      <v-container style="width: 1000px;">
        <v-select
          label="Укажите формат файла" 
          :items="formats"
          v-model="file_format"
          ></v-select>
          <v-btn id="download-button" @click="getFile()">Скачать файл</v-btn>
      </v-container>
      <v-container height="100px"></v-container>
      <hr>
  </div>
</template>

<script>
  import { yandexMap, ymapMarker } from 'vue-yandex-maps'
  export default {

    components: {
      yandexMap, 
      ymapMarker,
    },

    data: () => ({
      tableSearch: '',
      tableHeaders: [
        {
          text: 'Кластер',
          align: 'start',
          filterable: true,
          value: 'id_cluster',
        },
        { text: 'Тип ДТП', value: 'category', filterable: true, groupable: false, },
        { text: 'Дата', value: 'datetime', filterable: true, groupable: false, },
        { text: 'Количество пострадавших', value: 'injured', filterable: true, groupable: false, },
        { text: 'Количество погибших', value: 'deaths', filterable: true, groupable: false, },
        { text: 'Условия освещения', value: 'light', filterable: true, groupable: false, },
        { text: 'Дорожные условия', value: 'road_conditions', filterable: true, groupable: false, },
        { text: 'Погода', value: 'weather', filterable: true, groupable: false, },
      ],

      logged: false,

      //for init of maps
      settings: {
          apiKey: 'e70694c3-ce7f-4459-b7f6-be3d53e2cc8e',
          lang: 'ru_RU',
          coordorder: 'latlong',
          version: '2.1',
      },

      mapCenter: [59.9370, 30.3089],
      isShow: false,
      filter: [],
      currentMap: null,
      objectManager: null,
      accidentPoints: [],

      isCurse: true,
      user_point: {
        coords: null,
        points: null,
      },
      user_placemark: null,


      //for init of second map
      currentMap2: null,
      objectManager2: null,
      clasters: [],
      accidentInfo: [],

      fromBackendClasters: null,
      clasterCounter: 1,
      points: null,

      
      file_format: null,
      formats: [
        'csv',
        'xlsx',
        'json'
      ],

      //for map's filter
      isAllDays: true, 
      regions: [
        "Курортный район",
        "Кировский район",
        "Пушкинский район",
        "Московский район",
        "Фрунзенский район",
        "Петроградский район",
        "Калининский район",
        "Приморский район",
        "Василеостровский район",
        "Адмиралтейский район",
        "Красногвардейский район",
        "Петродворцовый район",
        "Колпинский район",
        "Невский район",
        "Кронштадтский район",
        "Центральный район",
        "Выборгский район",
        "Красносельский район"
        ],
      roadCondition: [
        "Отсутствие, плохая различимость горизонтальной разметки проезжей части",
        "Сухое",
        "Низкие сцепные качества покрытия",
        "Неправильное применение, плохая видимость дорожных знаков",
        "Неровное покрытие",
        "Нарушения в размещении наружной рекламы",
        "Отсутствие направляющих устройств и световозвращающих элементов на них",
        "Загрязненное",
        "Несоответствие дорожных ограждений предъявляемым требованиям",
        "Отсутствие, плохая различимость вертикальной разметки",
        "Плохая видимость светофора",
        "Неисправность светофора",
        "Неудовлетворительное состояние разделительной полосы",
        "Неисправное освещение",
        "Ограничение видимости",
        "Мокрое",
        "Заснеженное",
        "Гололедица",
        "Отсутствие освещения",
        "Отсутствие временных ТСОД в местах проведения работ",
        "Отсутствие тротуаров (пешеходных дорожек)",
        "Пыльное",
        "Отклонение верха головки рельса трамвайных (железнодорожных) путей, расположенных в пределах проезжей части, относительно покрытия, более чем на 2,0 см",
        "Обработанное противогололедными материалами",
        "Со снежным накатом",
        "Свежеуложенная поверхностная обработка",
        "Отсутствие пешеходных ограждений в необходимых местах",
        "Не установлено",
        "Отсутствие дорожных ограждений в необходимых местах",
        "Дефекты покрытия",
        "Недостаточное освещение",
        "Сужение проезжей части, наличие препятствий, затрудняющих движение транспортных средств",
        "Несоответствие люков смотровых колодцев и ливневой канализации предъявляемым требованиям",
        "Отсутствие дорожных знаков в необходимых местах",
        "Залитое (покрытое) водой",
        "Несоответствие железнодорожного переезда предъявляемым требованиям",
        "Недостатки зимнего содержания",
        "Отсутствие элементов обустройства остановочного пункта общественного пассажирского транспорта",
        "Плохая видимость световозвращателей, размещенных на дорожных ограждениях",
        "Неудовлетворительное состояние обочин"
        ],
      light: [
        "Светлое время суток",
        "Сумерки",
        "В темное время суток, освещение не включено",
        "В темное время суток, освещение включено",
        "В темное время суток, освещение отсутствует",
        "Не установлено"
      ],
      weather: [
        "Снегопад",
        "Ясно",
        "Метель",
        "Ураганный ветер",
        "Пасмурно",
        "Туман",
        "Дождь"
      ],
      category: [
        "Падение пассажира",
        "Наезд на пешехода",
        "Столкновение",
        "Иной вид ДТП",
        "Наезд на препятствие",
        "Съезд с дороги",
        "Опрокидывание",
        "Наезд на внезапно возникшее препятствие",
        "Падение груза",
        "Наезд на стоящее ТС",
        "Наезд на лицо, не являющееся участником дорожного движения, осуществляющее производство работ",
        "Наезд на велосипедиста",
        "Наезд на лицо, не являющееся участником дорожного движения, осуществляющее несение службы",
        "Наезд на животное",
        "Наезд на лицо, не являющееся участником дорожного движения, осуществляющее какую-либо другую деятельность",
        "Отбрасывание предмета"
      ],
      location: [
         "Остановка трамвая",
        "Надземный пешеходный переход",
        "Территориальное подразделение МВД России (либо его структурное подразделение)",
        "Нерегулируемый перекрёсток неравнозначных улиц (дорог)",
        "Нерегулируемый пешеходный переход, расположенный на участке улицы или дороги, проходящей вдоль территории школы или иного детского учреждения",
        "Остановка общественного транспорта",
        "Регулируемый пешеходный переход",
        "Эстакада, путепровод",
        "Автовокзал (автостанция)",
        "Зоны отдыха",
        "Крупный торговый объект (являющийся объектом массового тяготения пешеходов и (или) транспорта)",
        "Спортивные и развлекательные объекты",
        "Объект (здание, сооружение) религиозного культа",
        "Школа либо иная детская (в т.ч. дошкольная) организация",
        "Объект торговли, общественного питания на автодороге вне НП",
        "Выезд с прилегающей территории",
        "Иное образовательное учреждение",
        "Жилые дома индивидуальной застройки",
        "Подземный пешеходный переход",
        "Внутридворовая территория",
        "Объект строительства",
        "Иная образовательная организация",
        "СП ДПС (КПМ)",
        "Регулируемый пешеходный переход, расположенный на участке улицы или дороги, проходящей вдоль территории школы или иной детской организации",
        "Пешеходная зона",
        "Школа либо иное детское (в т.ч. дошкольное) учреждение",
        "Регулируемый перекрёсток",
        "Регулируемый пешеходный переход, расположенный на участке улицы или дороги, проходящей вдоль территории школы или иного детского учреждения",
        "Автостоянка (не отделённая от проезжей части)",
        "Одиночный торговый объект, являющийся местом притяжения транспорта и (или) пешеходов",
        "Иной объект",
        "Нерегулируемый перекрёсток",
        "Тротуар, пешеходная дорожка",
        "Нерегулируемый пешеходный переход",
        "Подход к мосту, эстакаде, путепроводу",
        "Регулируемый перекресток",
        "Административные здания",
        "Автостоянка (отделенная от проезжей части)",
        "Тоннель",
        "Кладбище",
        "Нерегулируемый пешеходный переход, расположенный на участке улицы или дороги, проходящей вдоль территории школы или иной детской организации",
        "Медицинские (лечебные) организации",
        "Аэропорт, ж/д вокзал (ж/д станция), речной или морской порт (пристань)",
        "Регулируемый ж/д переезд с дежурным",
        "Нерегулируемое пересечение с круговым движением",
        "Остановка маршрутного такси",
        "Лечебные учреждения",
        "Производственное предприятие",
        "Многоквартирные жилые дома",
        "АЗС",
        "Мост, эстакада, путепровод",
        "Нерегулируемый перекрёсток равнозначных улиц (дорог)",
        "Мост",
        "Регулируемый ж/д переезд без дежурного",
        "Нерегулируемый ж/д переезд"
      ],
      sliderTicks: [
        "Все время",
        "2.00 - 11.00", "11.00 - 16.00", 
        "16.00 - 21.00", "21.00 - 2.00"
      ],

      // for an authorized person
      rules: [
        value => (Number.isInteger(parseInt(value, 10))) || 'Введите целое число',
      ],
      quontityPatrolls: null,

      //Selected by any user
      filterParams: {
        roadCondition: "Отсутствие, плохая различимость горизонтальной разметки проезжей части",
        time: null,
        date: new Date().toISOString().substr(0, 10),
        region: "Пушкинский район",
        weather: "Снегопад",
        light: null,
        category: null,
        camera_number: null,
        location: null
      }
    }),

    methods: {
      drawTheTable(someClusters, target){
        this.accidentInfo = []
        console.log("TTTTTTTTAAAAAAAABBBBLLLLLEEEEE")
        console.log(someClusters)
        for (let j=0;j<someClusters.length;j++){
          axios.post(`${this.$store.state.backendUrl}/dtp/some/`, {"ids": someClusters[j].points}
        ).then(response => {
            for (let i=0;i<response.data.length;i++){
              this.accidentInfo.push(
                {
                  "id_cluster": target,
                  "id": response.data[i]["id"],
                  "datetime": response.data[i]["datetime"],
                  "category": response.data[i]["category"],
                  "deaths": response.data[i]["deaths"],
                  "injured": response.data[i]["injured"],
                  "light": response.data[i]["light"],
                  "weather": response.data[i]["weather"],
                  "road_conditions": response.data[i]["road_conditions"]
                }
              )
            }
          })
        }
      },

      onClickClaster(e) {
        let target = e.get('objectId')
        this.drawTheTable(this.fromBackendClasters, target)
      },

      onClickUserPoint(e) {
        if (this.isCurse) {
          if (this.user_placemark) {this.currentMap2.geoObjects.remove(this.user_placemark)}

          this.user_point.coords = e.get('coords')

          let filterData = {
            datetime: `${this.filterParams.date}T8:00:00Z`,
            time_group: this.filterParams.time - 1,
            regions: this.filterParams.region,
            weather: this.filterParams.weather,
            light: this.filterParams.light,
            categories: this.filterParams.category,
            nearby: this.filterParams.location,
            road_conditions: this.filterParams.roadCondition
          }
          if (this.isAllDays) filterData.datetime = null
          if (filterData.time_group === -1) filterData.time_group = null

          let filterDataString = "?"
          for (var key in filterData) {
              if (filterData[key]) filterDataString += `${key}=${filterData[key]}&`
          }
          filterDataString = filterDataString.substring(0, filterDataString.length - 1)

          axios.post(`${this.$store.state.backendUrl}/dtp/range/${filterDataString}`,{
              lat: this.user_point.coords[0],
              long: this.user_point.coords[1]
          }).then(response => {
              let points = []
              response.data.forEach(element => {
                points.push(element.id)
              })
              this.user_point.points = points
          })

          this.user_placemark = new ymaps.Placemark(this.user_point.coords)
          this.currentMap2.geoObjects.add(this.user_placemark)
          this.isCurse = false

          this.drawTheTable(this.user_point, this.clasterCounter)
        }
      },

      changeAccessToMap() {
        this.isCurse = !this.isCurse
      },

      deleteUserPoint() {
        this.currentMap2.geoObjects.remove(this.user_placemark)
        this.user_placemark = null
      },

      async getMapInstance(map) {
        if(map) {
          axios.get(`${this.$store.state.backendUrl}/dtp/list/?weather=Снегопад&regions=Пушкинский район&road_conditions=Отсутствие, плохая различимость горизонтальной разметки проезжей части`
          ).then(response => {
              for (let i=0;i<response.data.length;i++){
                let mapMarker = {
                  type: 'Feature',
                  id: response.data[i]["id"],
                  geometry: {
                      type: 'Point',
                      coordinates: [response.data[i]["lat"], response.data[i]["long"]]
                  }
                }
                this.accidentPoints.push(mapMarker)
              }
                try {
                  this.currentMap = map
                  this.objectManager = new ymaps.ObjectManager({
                      clusterize: true,
                      gridSize: 32,
                      clusterDisableClickZoom: true
                  })
                  this.currentMap.geoObjects.events.add('click', (e) => {
                    let target = e.get('objectId');
                    if (this.objectManager.clusters.getById(target)) {
                      let cluster = this.objectManager.clusters.getById(target)

                      let objects = cluster.properties.geoObjects
                      let buf = []
                      objects.forEach(element => {
                        buf.push(element.id)
                      });

                      axios.post(`${this.$store.state.backendUrl}/dtp/some/`,{
                        ids: buf
                      }).then(response => {
                        let data = response.data
                      })
                    }
                    else {
                      let point = this.objectManager.objects.getById(target)

                      axios.get(`${this.$store.state.backendUrl}/dtp/retrieve/${target}/`
                      ).then(response => {
                        let data = response.data
                        point.properties.hintContent = data.category + " " + data.datetime
                        point.properties.balloonContent = data.category + " " + data.datetime
                      })
                    }
                  })
                  try {
                      this.objectManager.add(this.accidentPoints)
                      this.currentMap.geoObjects.add(this.objectManager)
                  } catch (error) {
                      console.log('no points!')
                    }
                } catch (error) {
                console.log(error)
                }
            })
        }
      },

      async getMapInstance2(map2) {
        if(map2) {
          axios.get(`${this.$store.state.backendUrl}/dtp/list/?weather=Снегопад&regions=Пушкинский район&road_conditions=Отсутствие, плохая различимость горизонтальной разметки проезжей части`
          ).then(response => {
              let mapmarker = {
                type: 'Feature',
                id: response.data[0]["id"],
                geometry: {
                    type: 'Point',
                    coordinates: [response.data[0]["lat"], response.data[0]["long"]]
                }
              }
                this.clasters.push(mapmarker)

                try {
                  this.currentMap2 = map2
                  this.objectManager2 = new ymaps.ObjectManager({
                      clusterize: true,
                      gridSize: 32,
                      clusterDisableClickZoom: true
                  })

                  this.currentMap2.events.add('click', this.onClickUserPoint)

                  try {
                      this.objectManager2.add(this.clasters)
                      this.currentMap2.geoObjects.add(this.objectManager2)
                      this.currentMap2.geoObjects.events.add('click', this.onClickClaster)
                      this.objectManager2.removeAll()
                  } catch (error) {
                      console.log('no points!')
                    }
                } catch (error) {
                console.log(error)
                }
            })
        }
      },

        changeMap() {
          let filterData = {
            datetime: `${this.filterParams.date}T8:00:00Z`,
            time_group: this.filterParams.time - 1,
            regions: this.filterParams.region,
            weather: this.filterParams.weather,
            light: this.filterParams.light,
            categories: this.filterParams.category,
            nearby: this.filterParams.location,
            road_conditions: this.filterParams.roadCondition
          }

          if (this.isAllDays) filterData.datetime = null
          if (filterData.time_group === -1) filterData.time_group = null

          let filterDataString = ""
          for (var key in filterData) {
              if (filterData[key]) filterDataString += `${key}=${filterData[key]}&`
          }

          filterDataString = filterDataString.substring(0, filterDataString.length - 1)

          this.accidentPoints = []

          axios.get(`${this.$store.state.backendUrl}/dtp/list/?${filterDataString}`
          ).then(response => {
              for (let i=0;i<response.data.length;i++){
                let mapMarker = {
                  type: 'Feature',
                  id: response.data[i]["id"],
                  geometry: {
                      type: 'Point',
                      coordinates: [response.data[i]["lat"], response.data[i]["long"]]
                  }
                }
                this.accidentPoints.push(mapMarker)
              }
              this.objectManager.removeAll()
              this.objectManager.add(this.accidentPoints)
              }
            )
        },

        changeCameraMap() {
          let filterData = {
            datetime: `${this.filterParams.date}T8:00:00Z`,
            time_group: this.filterParams.time - 1,
            regions: this.filterParams.region,
            weather: this.filterParams.weather,
            light: this.filterParams.light,
            categories: this.filterParams.category,
            nearby: this.filterParams.location,
            road_conditions: this.filterParams.roadCondition
          }

          if (this.isAllDays) filterData.datetime = null
          if (filterData.time_group === -1) filterData.time_group = null

          let filterDataString = "?"
          for (var key in filterData) {
              if (filterData[key]) filterDataString += `${key}=${filterData[key]}&`
          }

          filterDataString = filterDataString.substring(0, filterDataString.length - 1)
          this.clasters = []
          this.fromBackendClasters = []
          axios.get(`${this.$store.state.backendUrl}/claster/${this.quontityPatrolls}/${filterDataString}` 
          ).then(response => {
            this.fromBackendClasters = response.data
            for (let i=0; i<response.data.length;i++){
              let claster = {
                type: 'Feature',
                id: this.clasterCounter,
                geometry: {
                    type: 'Point',
                    coordinates: [response.data[i]["lat"], response.data[i]["long"]]
                },
                properties: {
                    hintContent: response.data[i]["points"],
                },
                options: {
                    preset: "islands#dotIcon",
                    iconColor: "red"
                }
              }
              
              this.clasterCounter += 1
              this.clasters.push(claster)
            }

            this.objectManager2.removeAll()
            this.objectManager2.add(this.clasters)
            console.log("Updated2!")
          })
        },

        getFile() {
          axios.post(`${this.$store.state.backendUrl}/file/get/`, this.fromBackendClasters).then(
            response => {
              window.open(`${this.$store.state.backendUrl}/file/get/${response.data}/${this.file_format}/`);
            }
          )
        },
    },

    created: function(){
      if (this.$store.state.token) {
        this.logged = true 
      }
      // console.log(this.isCurse)
      // console.log(this.user_placemark == null)
    }
}
</script>

<style scoped>
    #map {
        width: 800px; 
        height: 800px;
        margin: 0 auto;
        margin-top: 20px;
    }
    #map2 {
        width: 800px; 
        height: 800px;
        margin: 0 auto;
        margin-top: 20px;
    }
    .report-col {
        margin-left: 300px;
    }
    .report-msg {
        margin-bottom: 30px;
    }
    .row {
      padding: 0px 30px;
    }
    label {
       color: black; 
       font-weight: 600;
    }
    #isBigger {
      height: 800px;
    }
    #stat {
      margin: auto;
      width: auto;
    }

    th {
      background-color: #212F3C;
      color: white;
    }

    #download-button, #access-button, #delete-button {
      position: relative;
      left: 50%;
      transform: translate(-50%, 0);
      width: 300px;
    }

    #access-button, #delete-button {
      margin-top: 30px;
      margin-right: 10px;
    }

    .two-buttons {
      margin: auto;
      padding-right: 320px;
    }

</style>

