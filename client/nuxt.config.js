const { parsed } = require("dotenv").config({
  path:
    "environments/.env" +
    (process.env.NODE_ENV == "development" ? "" : "." + process.env.NODE_ENV),
});

export default {
  ssr: false,
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: "NeRF",
    htmlAttrs: {
      lang: "en",
    },
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
      { name: "format-detection", content: "telephone=no" },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },

  loading: false,

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ["ant-design-vue/dist/antd.css", "~/css/main.css"],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ["@/plugins/antd-ui", "@/plugins/axios"],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: ["@nuxtjs/moment", "@nuxtjs/dotenv"],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    "@nuxtjs/i18n",
  ],

  i18n: {
    locales: [
      { code: "en", file: "en.json" },
      { code: "ja", file: "ja.json" },
    ],
    defaultLocale: "en",
    langDir: "locales",
    vueI18n: {
      fallbackLocale: "en",
    },
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: process.env.API_BASE_URL,
  },

  router: {
    middleware: ["lang"],
  },

  env: { ...parsed },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
  server: {
    host: '0.0.0.0', // default: localhost
    port: process.env.PORT
  }
};
