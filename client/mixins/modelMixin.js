import * as CONST from "@/constants/index.js";
export default {
  computed: {
    currentParamConfig() {
      return this.model?.trainingParams?.find(
        (config) => config.id == this.configId
      );
    },
  },
  methods: {
    snakeCaseToTitleCase(str) {
      return str
        .split("_")
        .map(
          (word, index) =>
            (index === 0 ? word.charAt(0).toUpperCase() : word.charAt(0)) +
            word.slice(1)
        )
        .join(" ");
    },
  },
};
