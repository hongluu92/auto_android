let API_BASE_URL = process.env.API_BASE_URL;

export const state = () => ({
  roles: null,
  users: null,
});

export const mutations = {
  setRoles(state, roles) {
    state.roles = roles;
  },
  setUsers(state, users) {
    state.users = users;
  },
};

export const actions = {
  async login({ commit }, payload) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/login`,
      payload
    );
    return data;
  },
  async getRoles({ commit }) {
    const { data } = await this.$axios.get(`${API_BASE_URL}/api/v1/roles`);
    commit("setRoles", data.data);
    return data.data;
  },
  async register({ commit }, payload) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/user`,
      payload
    );
    return data;
  },
  async changePassword({ commit }, payload) {
    const { data } = await this.$axios.put(
      `${API_BASE_URL}/api/v1/password`,
      payload
    );
    return data;
  },
  async fetchUsers({ commit }) {
    const { data } = await this.$axios.get(`${API_BASE_URL}/api/v1/users`);
    commit("setUsers", data.data);
    return data;
  },
  async deleteUser({ commit }, payload) {
    const { data } = await this.$axios.delete(
      `${API_BASE_URL}/api/v1/user/${payload.id}`,
      {
        data: payload,
      }
    );
    return data;
  },
  async restoreUser({ commit }, id) {
    const { data } = await this.$axios.put(`${API_BASE_URL}/api/v1/user/${id}`);
    return data;
  },
  async fetchDeletedUsers({ commit }) {
    const { data } = await this.$axios.get(
      `${API_BASE_URL}/api/v1/users/deleted`
    );
    commit("setUsers", data.data);
    return data;
  },
  async forgotPassword({ commit }, payload) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/forgot-password`,
      payload
    );
    return data;
  },
  async resetPassword({ commit }, payload) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/reset-password`,
      payload
    );
    return data;
  },
  async getUserById({ commit }, id) {
    const { data } = await this.$axios.get(`${API_BASE_URL}/api/v1/user/${id}`);
    return data.data[0];
  },
  async updateUser({ commit }, payload) {
    const { data } = await this.$axios.post(
      `${API_BASE_URL}/api/v1/user/${payload.id}`,
      payload
    );
    return data;
  },
};
