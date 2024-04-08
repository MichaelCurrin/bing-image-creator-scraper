import { createApp } from "https://unpkg.com/vue@3.2/dist/vue.esm-browser.js";

const app = createApp({
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      const response = await fetch('creation-data.json');
      const data = await response.json();
      this.folders = data;
    }
  },
  data() {
    return {
      folders: {}
    }
  },
  template: `
      <div v-for="folder in folders" :key="folder.folderName">
          <h2>{{ folder.folderName }}</h2>

          <p>{{ folder.description }}</p>

          <a :href="folder.url">{{ folder.url }}</a>

          <div v-for="image in folder.images" :key="image">
              <img :src="image" loading="lazy">
          </div>
      </div>
    `,
});

app.mount("#app");
