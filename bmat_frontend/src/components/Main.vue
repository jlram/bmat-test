<template>
  <div class="hello">
    <v-row>
      <v-col cols="12">
        <h1 class="pb-5">{{ msg }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-spacer/>
      <v-col cols="6">
        <v-file-input
          v-model="file"
          id="csv"
          accept="csv"
          label="Open CSV to load metadata"
          @change="uploadCSV"
        />
      </v-col>
      <v-spacer/>
    </v-row>
    <v-row>
      <v-spacer/>
      <v-col cols="10">
        <v-data-table
          v-if="showTable"
          :headers="headers"
          :items="works"
          :items-per-page="5"
          class="elevation-1"
        >
        <!-- Custom slots -->
         <template v-slot:[`item.contributors`]="{ item }">
            <p v-for="[index, contributor] of item.contributors.entries()" :key="contributor.id">
              {{ contributor.name + (index !== item.contributors.length -1 ? ', ' : '')}}
            </p>
          </template>

         <template v-slot:[`item.sources`]="{ item }">
            <p v-for="source of item.sources" :key="source.id">
              {{ 'ID:' + source.id_source  + ' LABEL:' + source.name }}
            </p>
          </template>
        </v-data-table>
      </v-col>
      <v-spacer/>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'Main',

  data: () => ({
    file: undefined,
    headers: [
        {
          text: 'Title',
          align: 'start',
          sortable: false,
          value: 'title',
        },
        { text: 'Contributors', value: 'contributors' },
        { text: 'ISWC', value: 'iswc' },
        { text: 'ID from Source', value: 'sources' }
    ],
    showTable: true,
    works: []
  }),

  props: {
    msg: String
  },

  created () {
    this.loadWorks()
  },

  methods: {
    uploadCSV () {
      if (this.file) {
        var formData = new FormData();
        formData.append('file', this.file)
        this.$http.post('http://127.0.0.1:8000/import_csv/', formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(() => {
          this.loadWorks()
        })
      }
    },
    loadWorks () {
      this.$http.get('http://127.0.0.1:8000/works/').then((response) => {
        this.works = response.data
      })
    }
  }
}
</script>

<style scoped>
  #csv {
    position: relative;
    top: 25px;
  }
</style>>
