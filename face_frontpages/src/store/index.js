import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    account: "",
    work_id: "",
    test: [],
  },
  mutations: {
    account_updata(state, account) {
      state.account = account
    },
    work_id_updata(state, work_id) {
      state.work_id = work_id
    },
    SOCKET_webPhoneUpdate: (state, data) => {
      state.test.push(data);
      // state.phone_info.sort(state.phone_info.timestr)
      console.log('vuex get phone_info')
    },
    SOCKET_webEvidenceUpdate(state, data) {
      console.log('vuex get webEvidenceUpdate')
      state.test.push(data);
    },
    SOCKET_webPhoneUpdateData(state, data) {
      console.log('vuex get webPhoneUpdate')
      state.test = data;
      console.log(state.test)
    },
  },
  actions: {},
  modules: {},
})
