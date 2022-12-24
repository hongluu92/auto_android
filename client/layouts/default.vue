<template>
  <a-config-provider :locale="locale">
    <a-layout>
      <Nav />
      <Breadcrumb style="margin-top: 86px; margin-bottom: 8px" />

      <nuxt class="card-atv"> </nuxt>
      <Footer />
    </a-layout>
  </a-config-provider>
</template>

<script>
import ja_JP from "ant-design-vue/lib/locale-provider/ja_JP";
import en_US from "ant-design-vue/lib/locale-provider/en_US";
import Breadcrumb from "@/components/Breadcrumb";
export default {
  middleware: "auth",
  components: { Breadcrumb },
  data() {
    return {
      locale: {},
    };
  },
  async mounted() {
    const curLocale = localStorage.getItem("lang");
    localStorage.setItem("lang", curLocale);
    if (curLocale === "ja") this.locale = ja_JP;
    else this.locale = en_US;
  },
};
</script>