<template>
    <v-card
      class="mx-auto overflow-visible pt-5 rounded-lg"
      color="white"
      variant="outlined"
    >
      <v-sheet
        class="v-sheet--offset mx-auto custom-scrollbar position-relative"
        color="rgba(0, 0, 0, 0.5)"
        elevation="12"
        max-width="calc(100% - 32px)"
        rounded="lg"
        style="overflow-x: auto; position: relative;"
      >
        <v-sparkline
          :model-value="sismicDetectionSetValues"
          :gradient-direction="gradientDirection"
          auto-draw
          auto-draw-duration="15000"
          color="red"
          line-width="1.5"
          max="1"
          min="0"
          smooth="15"
          padding="16"
          height="220"
          width="3000"
          style="width: 3000px;"
        ></v-sparkline>
        <v-sparkline
          :model-value="dataSetValues"
          :gradient="gradient"
          :gradient-direction="gradientDirection"
          auto-draw
          auto-draw-duration="15000"
          color="white"
          line-width="1.5"
          max="1"
          min="0"
          smooth="15"
          padding="16"
          height="220"
          width="3000"
          style="width: 3000px; position: absolute; top: 0; left: 0; z-index: 1;"
        ></v-sparkline>
      </v-sheet>
  
      <v-card-text class="pt-2">
        <div class="subheading font-weight-light text-grey">
          {{this.dataSet[0] && this.dataSet[0].second ? `Date: ${this.dataSet[0].second.slice(0, 10)}` : ''}}
        </div>
      </v-card-text>
    </v-card>
  </template>

<script>
const gradients = [
  ['#ffd200', '#ffd244', '#ffd277', '#ffd2bb', '#ffd2dd'],
  ['#42b3f4'],
  ['red', 'orange', 'yellow'],
];
export default {

  data: () => ({
    gradient: gradients[0],
    gradientDirection: 'right',
  }),
  props: {
    dataSet: {
      type: Array,
      required: true
    },
  },
  mounted () {
  },
  computed: {
    dataSetValues() {
      if(this.dataSet) {
        return this.dataSet.map(item=>item.normalized_filtered_velocity);
      } else {
        return [];
      }
    },
    sismicDetectionSetValues() {
      if(this.dataSet) {
        return this.dataSet.map(item=>item.prediction);
      } else {
        return [];
      }
    },
  }
}
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #42b3f4 #f0f0f0;
}

/* For WebKit browsers */
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #42b3f4;
  border-radius: 10px;
  border: 2px solid #f0f0f0;
}
</style>