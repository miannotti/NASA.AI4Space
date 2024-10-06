<template>
  <v-container fluid>
    <video autoplay loop muted playsinline class="video-background">
      <source src="@/assets/moon-video-2.mp4" type="video/mp4" />
      Your browser doesn't support video
    </video>

    <div class="video-overlay"></div>
    <v-row>
      <Navbar />
    </v-row>
    <v-row style="max-width: 100%;">
      <v-col
        cols="12"
        md="9"
      >
        <WaveVisualizer
          :data-set="moonDataset"
          :key="waveVisualizerComponentKey"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="selectedValue"
          label="Select Date to Visualize"
          :items="selectOptions"
          hide-details
          density="compact"
          class="mb-2"
          variant="outlined"
        ></v-select>
        <ModelInfo />
      </v-col>
    </v-row>
    <v-row style="max-width: 100%;">
      <v-col
        cols="12"
        md="4"
      >
        <v-row>
          <v-col
            cols="12"
          >
          <v-card
            class="mx-auto overflow-visible pa-5"
            color="white"
            variant="outlined"
          >
            <div class="text-body-1 mb-2">Frequency Spectrum</div>
            <v-img
                :src="fourierImageSrc"
                height="200"
            />
          </v-card>
          </v-col>
        </v-row>
      </v-col>
      <v-col
        cols="12"
        md="8"
      >
        <RawRegistersVisualizer
          :icon="'moon'"
          :data-set="moonDataset"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import moonData1 from '@/data/moonData.json';
import moonData2 from '@/data/moonData2.json';
import moonData3 from '@/data/moonData3.json';
import moonData4 from '@/data/moonData4.json';

import fourierImage1 from '@/assets/fourier-transform-1.jpg';
import fourierImage2 from '@/assets/fourier-transform-2.jpg';
import fourierImage3 from '@/assets/fourier-transform-3.jpg';
import fourierImage4 from '@/assets/fourier-transform-4.jpg';
export default {
  data: () => ({
    selectedValue: 'Option 1',
    waveVisualizerComponentKey: 0,
    fourierImageSrc: new URL('@/aassets/fourier-transform-1.jpg', import.meta.url).href,
    selectOptions: [
      { title: 'Option 1', value: 'Option 1' },
      { title: 'Option 2', value: 'Option 2' },
      { title: 'Option 3', value: 'Option 3' },
      { title: 'Option 4', value: 'Option 4' },
    ],
  }),
  computed: {
    moonDataset() {
      switch (this.selectedValue) {
        case 'Option 1':
          this.fourierImageSrc = fourierImage1;
          return moonData1;
        case 'Option 2':
        this.fourierImageSrc = fourierImage2;
          return moonData2;
        case 'Option 3':
          this.fourierImageSrc = fourierImage3;
          return moonData3;
        case 'Option 4':
          this.fourierImageSrc = fourierImage4;
          return moonData4;
      }
    },
  }
}
</script>
<style scoped>
.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
}
</style>