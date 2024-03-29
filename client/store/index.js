let API_BASE_URL = process.env.API_BASE_URL;
import moment from "moment";
import cloneDeep from "lodash.clonedeep";

export const state = () => ({
  scriptList: [],
  scriptListTotal: 0,
  paramList: null,
  model: null,
  script: null , 
  actionList: []
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
  setScript(state, payload) {
    state.script = payload;
  },
  setActions(state, payload) {
    state.actionList = payload;
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
      data.sort((a, b) => moment(b.updated_at).diff(moment(a.updated_at)))
    );
    // commit("setScriptListTotal", data.metadata.total);
    // commit("setUsersWithModels", data.metadata.users);
    return data;
  },
  async deleteScript({ commit }, id) {
    const { data } = await this.$axios.delete(`${API_BASE_URL}/api/v1/scripts/${id}`);
    return data;
  },
  async createScript({ commit }, param) {
    const { data } = await this.$axios.post(`${API_BASE_URL}/api/v1/scripts/`,param );
    return data;
  },
  async updateScript({ commit }, param) {
    const { data } = await this.$axios.put(`${API_BASE_URL}/api/v1/scripts/`, param );
    return data;
  },
  async getScript({ commit }, id) {
    let script = null
    if (state.scriptList && state.scriptList.length > 0){
      script = state.scriptList.filter(x => x.id == id)[0]
    }
    const { data }  =  await this.$axios.get(`${API_BASE_URL}/api/v1/scripts/${id}`);
    script =  data;
    commit("setScript",script);
    return script
  },
  async getActions({ commit }, script_id) {
    const { data }  =  await this.$axios.get(`${API_BASE_URL}/api/v1/script-actions?script_id=${script_id}`);
    let actions =  data;
    if (actions)
      return actions
    else return []
  },
  async updateAction({ commit }, payload) {
    console.log(payload)
    const { data }  =  await this.$axios.put(`${API_BASE_URL}/api/v1/script-actions?script_id=${payload.script_id}`, payload);
    let action =  data;
    return action
  },
  async createAction({ commit }, payload) {
    const { data }  =  await this.$axios.post(`${API_BASE_URL}/api/v1/script-actions?script_id=${payload.script_id}`, payload);
    let action =  data;
    return action
  },
  async reload_current_img ({ commit }){
    const { data }  =  await this.$axios.post(`${API_BASE_URL}/api/v1/script-actions/reload-current-img`);
  },
  async runAction({ commit }, payload) {
    const { data }  =  await this.$axios.post(`${API_BASE_URL}/api/v1/script-actions/run`, payload);
  },
  getImgSrc({ commit }, img_path){
    return `${API_BASE_URL}/static/imgs/${img_path}`
  }
};
