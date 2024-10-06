<template>
  <v-card
    class="mx-auto overflow-visible pa-5"
    color="white"
    variant="outlined"
  >
    <div v-if="!item" class="text-body-2 text-grey">
      Click on a record to view details
    </div>
    <div v-else>
      <div v-for="(value, i) in item">
        <span class="text-caption nmb-2 d-block text-grey pb-0 mb-0">{{ i }}</span>
        <span class="text-body-2">{{ value }}</span>
      </div>
    </div>
  </v-card>
</template>

<script>
  export default {
    data: () => ({
    }),
    props: {
    item: {
      type: Object,
      required: false
    },
  },
  }
</script>
