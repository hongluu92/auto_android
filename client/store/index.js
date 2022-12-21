let API_BASE_URL = process.env.API_BASE_URL;
import moment from "moment";
import cloneDeep from "lodash.clonedeep";

export const state = () => ({
  scriptList: [],
  scriptListTotal: 0,
  paramList: null,
  model: null,
});

export const mutations = {
  setScriptList(state, payload) {
    state.scriptList = payload;
  },
  setScriptListTotal(state, payload) {
    state.scriptListTotal = payload;
  },
  setParamList(state, payload) {
    state.paramList = payload;
  },
  setCurrentModel(state, payload) {
    // retain the config having config id == "new" if the new trainingParams array length is shorter than the current trainingParams array length
    let newConfig = state.model?.trainingParams?.find(
      (config) => config.id == "new"
    );
    let currentConfigLength = cloneDeep(state.model?.trainingParams?.length);
    state.model = payload;
    if (
      newConfig &&
      currentConfigLength > state.model?.trainingParams?.length &&
      !state.model.forceDeleteConfig
    )
      state.model.trainingParams.push(newConfig);
  },
};

export const actions = {
  async uploadFiles({ commit }, body) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/upload`,
      body
    );
    return data;
  },
  async fetchScriptList({ commit }, params) {
    const { data } = await this.$axios.get(`${API_BASE_URL}/api/v1/scripts`, {
      params,
    });
    commit(
      "setScriptList",
      data.items.sort((a, b) => moment(b.updated_at).diff(moment(a.updated_at)))
    );
    commit("setScriptListTotal", data.metadata.total);
    commit("setUsersWithModels", data.metadata.users);
    return data;
  },
  async fetchParamList({ commit }) {
    const { data } = await this.$axios.get(`${API_BASE_URL}/api/v1/parameters`);
    commit("setParamList", data.items?.[0].json_data);
    return data;
  },
  async updateModel({ commit }, payload) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/models/${payload.id}`,
      payload
    );
    commit("setCurrentModel", data.data[0]);
    return data;
  },
  async processModel({ commit }, id) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/process/${id}`
    );
    return data;
  },
  async cancelModel({ commit }, { configId, isRemeshing }) {
    const { data } = await this.$axios.delete(
      `${API_BASE_URL}/api/v1/process/${configId}${
        isRemeshing ? "?remeshing=true" : ""
      }`
    );
    return data;
  },
  async continueProcessingModel({ commit }, payload) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/continue-processing`,
      payload
    );
    return data;
  },
  async getModelById({ commit }, id) {
    const { data } = await this.$axios.get(
      `${API_BASE_URL}/api/v1/models/${id}`
    );
    commit("setCurrentModel", data);
    return data;
  },
  async removeBackground({ commit }, modelID) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/remove-background/${modelID}`
    );
    return data;
  },
  async getEstimatedTime({ commit }, modelID) {
    const { data } = await this.$axios.get(
      `${API_BASE_URL}/api/v1/remove-background/${modelID}`
    );
    return data.data;
  },
  async deleteImages({ commit }, payload) {
    const { data } = await this.$axios.delete(
      `${API_BASE_URL}/api/v1/model/images/`,
      { data: payload }
    );
    return data;
  },
  async extractImages({ commit }, modelID) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/extract-images/${modelID}`
    );
    return data;
  },
  async extractPoses({ commit }, id) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/extract-poses/${id}`
    );
    return data;
  },
  async unzip({ commit }, modelID) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/unzip/${modelID}`
    );
    return data;
  },
  async deleteConfig({ commit }, id) {
    const { data } = await this.$axios.delete(
      `${API_BASE_URL}/api/v1/model/meta/${id}`
    );
    return data;
  },
  async deleteScipt({ commit }, id) {
    const { data } = await this.$axios.delete(
      `${API_BASE_URL}/api/v1/script/${id}`
    );
    return data;
  },
  async createWorkspace({ commit }, modelID) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/workspace/${modelID}`
    );
    return data;
  },
  async remesh({ commit }, id) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/remesh/${id}`
    );
    return data;
  },
  async uploadPoses({ commit }, formData) {
    let configId = formData.get("configId");
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/poses/${configId}`,
      formData
    );
    return data;
  },
};
