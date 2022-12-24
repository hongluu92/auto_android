<template>
  <a-layout-footer style="text-align: center">
    <span
      >Copyright © {{ new Date().getFullYear() }} Ruby</span
    >
  </a-layout-footer>
</template>

<script>
import baseMixin from "@/mixins/baseMixin";
export default {
  name: "Footer",
  mixins: [baseMixin],
};
</script>

<style>
</style>