<template>
  <v-card
    class="mx-auto overflow-visible pa-5"
    color="white"
    variant="outlined"
  >
    <span class="text-body-1">XGBoost Classification Report</span>
    <v-row>
        <v-col cols="6" v-for="(item) in items">
            <div v-for="(value, i) in item">
                <span class="text-caption nmb-2 d-block text-grey pb-0 mb-0">{{ i }}</span>
                <span class="text-body-2">{{ value }}</span>
            </div>
        </v-col>
    </v-row>
  </v-card>
</template>
  
<script>
export default {
    data: () => ({
    items: [
        {
            Case: 'No seismic event',
            Precision: '0.94',
            Recall: '0.88',
            F1score: '0.91',
            Support: '450',
        },
        {
            Case: 'Seismic event',
            Precision: '0.78',
            Recall: '0.88',
            F1score: '0.83',
            Support: '225',
        },
    ]
    }),
}
</script>
<style scoped>
.nmb-2 {
    padding-bottom: 4px;
}
</style>