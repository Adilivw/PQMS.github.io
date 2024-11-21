import Vue from 'vue'
import Vuex from 'vuex'
import coatingApi from '@/api/coating'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    realtimeData: null,
    coatingData: [],
    spcData: null,
    correlationData: null,
    loading: false,
    error: null
  },
  
  mutations: {
    SET_REALTIME_DATA(state, data) {
      state.realtimeData = data
    },
    SET_COATING_DATA(state, data) {
      state.coatingData = data
    },
    SET_SPC_DATA(state, data) {
      state.spcData = data
    },
    SET_CORRELATION_DATA(state, data) {
      state.correlationData = data
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async fetchRealtimeData({ commit }) {
      try {
        commit('SET_LOADING', true)
        const response = await coatingApi.getRealtimeData()
        commit('SET_REALTIME_DATA', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchCoatingData({ commit }, params) {
      try {
        commit('SET_LOADING', true)
        const response = await coatingApi.getCoatingData(params)
        commit('SET_COATING_DATA', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchSPCData({ commit }, params) {
      try {
        commit('SET_LOADING', true)
        const response = await coatingApi.getSPCAnalysis(params)
        commit('SET_SPC_DATA', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchCorrelationData({ commit }) {
      try {
        commit('SET_LOADING', true)
        const response = await coatingApi.getCorrelationAnalysis()
        commit('SET_CORRELATION_DATA', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}) 