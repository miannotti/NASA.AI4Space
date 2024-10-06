<template>
  <v-row>
    <v-col cols="12" md="7">
      <v-card
        class="mx-auto"
        color="rgba(0, 98, 255, 0.3)"
      >
        <v-card-item>
          <v-card-title>
            Data set
          </v-card-title>
          <template v-slot:append>
            <v-img
              :src="imageSrc"
              contain
              width="30"
              height="30"
            />
          </template>
        </v-card-item>

        <v-divider></v-divider>

        <v-virtual-scroll
          :items="dataSet"
          height="225"
          item-height="48"
        >
          <template v-slot:default="{ item }">
            <v-list-item
              :subtitle="`${item.prediction ? 'ALARM ON' : 'Alarm off' }`"
              :title="item.second"
              :class="item.prediction ? 'text-red' : 'text-white'"
            >
              <template v-slot:append>
                <v-btn
                  icon="mdi-eye"
                  size="x-small"
                  variant="tonal"
                  @click="seeItemDetail(item)"
                ></v-btn>
              </template>
            </v-list-item>
          </template>
        </v-virtual-scroll>
      </v-card>
    </v-col>
    <v-col cols="12" md="5">
      <RegistrationDetail
        :item="itemDetail"
      />
    </v-col>
  </v-row>
</template>
<script>
import RegistrationDetail from './RegistrationDetail.vue';
import moonImg from '@/assets/full-moon.gif';
import marsImg from '@/assets/mars.gif';

export default {
  data: () => ({
    items: Array.from({ length: 1000 }, (k, v) => v + 1),
    itemDetail: null,
    imageSrc: null
  }),
  props: {
    icon: {
      type: String,
      required: false
    },
    dataSet: {
      type: Array,
      required: true
    },
  },
  mounted() {
    this.imageSrc = this.icon === 'moon' ? moonImg : marsImg;
  },
  methods: {
    seeItemDetail(item) {
      this.itemDetail = item;
    }
  }
}
</script>