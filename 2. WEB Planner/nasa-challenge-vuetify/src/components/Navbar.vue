<template>
    <v-app-bar app color="rgba(0,0,0,0.7)">
      <v-toolbar-title>Seismic Planner</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/">Home</v-btn>
      <v-btn text to="/mars-visualizer">Explore Mars</v-btn>
      <v-btn text to="/moon-visualizer">Explore Moon</v-btn>
    </v-app-bar>
  </template>
  
  <script>
  export default {
    name: 'Navbar'
  }
  </script>
  
  <style scoped>
  </style>