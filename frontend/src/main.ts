import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css"; // Іконки
import "@fontsource/roboto/100.css";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css"; // Основний текст
import "@fontsource/roboto/500.css"; // Заголовки та кнопки
import "@fontsource/roboto/700.css";
import "@fontsource/roboto/900.css";

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "dark", // Ти ж любиш термінали, тому темна тема за замовчуванням :)
  },
});

createApp(App).use(vuetify).mount("#app");
