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
  </div>
</template>

<script>
export default {
  name: 'Main',

  data: () => ({
    file: undefined,
  }),

  props: {
    msg: String
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
        .then((result) => {
          console.log(result.data)
        })
      }
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
