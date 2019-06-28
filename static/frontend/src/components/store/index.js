import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
import {HTTP} from '../../http-common'

export const store = new Vuex.Store({
  state: {
    currentDoc: {
      data: {},
      status: {
        widgetIsValid: {},
        tableUnit: {
          sort: {field: "", order: -1},
          selected: []
        }
      }
    },
    docs: [],
  },
  getters: {
    currentDoc: state => {
      return state.currentDoc.data
    },

    currentDocStatus: state => {
      return state.currentDoc.status
    }
  },
  mutations: {
    SETcurrentDoc: (state, data) => {
      state.currentDoc.data = data
    },
  },
  actions: {
    GETcurrentDoc: (state, docType, id) => {

    }
  },
});