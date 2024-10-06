<template>
  <v-container class="fill-height background-color overflow-visible" fluid>
    <video autoplay loop muted playsinline class="video-background">
      <source src="@/assets/space-video.mp4" type="video/mp4" />
      Your browser doesn't support video
    </video>
    <!-- Capa de superposición -->
    <div class="video-overlay"></div>
    <v-responsive
      class="align-centerfill-height mx-auto overflow-visible"
    >

      <v-row class="overflow-visible">
        <v-col cols="12" md="4" class="overflow-visible">
          <div class="overflow-visible position-relative clickeable-link">
            <v-img
              :src="imageSrc"
              max-width="400"
              contain
              class="mx-auto floating-planets overflow-visible"
              @click="goToMoonVisualizer()"
            />
            <p class="text-overline text-center position-absolute planet-text-position">GET TO KNOW THE MOON</p>
          </div>
        </v-col>

        <v-col cols="12" md="4" class="d-flex justify-center align-center">
          <p class="text-h1 font-weight-light text-center">Seismic <span class="text-h2">Planner</span></p>
        </v-col>
        <v-col cols="12" md="4" class="overflow-visible">
          <div class="overflow-visible position-relative clickeable-link">
            <v-img
              :src="imageMarsSrc"
              max-width="400"
              contain
              class="mx-auto floating-planets overflow-visible"
              @click="goToMarsVisualizer()"
            />
            <p class="text-overline text-center position-absolute planet-text-position">GET TO KNOW MARS</p>
          </div>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    imageSrc: new URL('@/assets/moon-and-mars-01.png', import.meta.url).href,
    imageMarsSrc: new URL('@/assets/moon-and-mars-02.png', import.meta.url).href
  }),
  methods: {
  goToMoonVisualizer() {
    this.$router.push('/moon-visualizer')
  },
  goToMarsVisualizer() {
    this.$router.push('/mars-visualizer')
  }
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
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 32, 1) 50%);
}
  .background-color {
    background-color: rgb(0, 0, 32);
  }

  @keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0);
  }
}

.floating-planets {
  animation: float 4s ease-in-out infinite;
}
.floating-mars {
  animation: float 6s ease-in-out infinite;
}

.clickeable-link {
  cursor: pointer;
}

.overflow-visible {
  overflow: visible !important;
}

.planet-text-position {
  top: 80%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
}
</style>
