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
    catlgs: {
      department: {},
      stock: {},
      person: {},
      device: {},
      deviceType: {},
      nomenclature: {},
    },
  },
  getters: {
    currentDoc: state => {
      return state.currentDoc.data
    },

    currentDocStatus: state => {
      return state.currentDoc.status
    },

    catlgExist: state => catlgType => {
      if (catlgType in state.catlgs) {
        return true
      } else {
        return false
      }
    },

    GETcatlgItem: state => (catlgType, id) => {
        return state.catlgs[catlgType][id]
    },

    GETcatlgItemLabel: state => (catlgType, id) => {
      if (id in state.catlgs[catlgType]){
        return state.catlgs[catlgType][id]['label']
      }
    },

    GETcatlg: state => catlgType => {
      return state.catlgs[catlgType]
    },

    GETcatlgByLabel: state => (catlgType, label) => {
      var catlg = []
      for (let key in state.catlgs[catlgType]) {
        if (state.catlgs[catlgType][key]['label'].toLowerCase().indexOf(label.toLowerCase()) != -1) {
          catlg.push(state.catlgs[catlgType][key])
        }
      }
      return catlg
    },

    GETdocs: state => {
      return state.docs
    },


  },
  mutations: {
    SETcurrentDoc: (state, data) => {
      state.currentDoc.data = data
    },

    UPDcurrentDoc: (state, [key, value]) => {
      if (value instanceof Event) {
        state.currentDoc.data[key] = value.data
      } else {
        state.currentDoc.data[key] = value
      }
    },

    SETdocs: (state, data) => {
      state.docs = data
    },

    SETcatlgItem: (state, [catlgType, item]) => {
      Vue.set(state.catlgs[catlgType], item.id, item)
    },

    SETcatlgItemLabel: (state, [catlgType, id, label]) => {
      Vue.set(state.catlgs[catlgType][id], 'label', label)
    },



  },
  actions: {
    FETCHcurrentDoc: async ({commit, dispatch, getters}, [docType, id]) => {
      let response = await HTTP.get(docType + '/' + id + '/')
      dispatch('FETCHwidgetInitCatlg', [response.data['table_unit'], {device: 'device', person: 'person'}])

      for (let key in response.data){
        if ((getters.catlgExist(key)) && (response.data[key])) {
          await dispatch('FETCHcatlgItem', [key, response.data[key]])
        }
      }
      commit('SETcurrentDoc', response.data)
    },

    FETCHdocs: async ({commit, dispatch, getters}, docType) => {
      let response = await HTTP.get(docType + '/')
      let DocsReady = response.data
      commit('SETdocs', DocsReady)
      dispatch('FETCHdependentCatlg', DocsReady)
    },

    FETCHwidgetInitCatlg: async ({commit, dispatch, getters}, [tableUnit, fieldsMap]) => {
      for (var fieldTableUnit in fieldsMap) {
        var catlgType  = fieldsMap[fieldTableUnit]
        var catlgToLoad = _.uniq(_.map(tableUnit, _.property(fieldTableUnit)))
        catlgToLoad = catlgToLoad.filter(function (el) {
            return el != null;
          });
         dispatch('FETCHcatlgItem', [catlgType, catlgToLoad])
      }
    },

    FETCHcatlgItem: async ({commit, dispatch, getters}, [catlgType, id]) => {
      try {
        if (!Array.isArray(id)){
          var response = await HTTP.get(catlgType + '/'+ id + '/')
          var catlgItemFetch = [response.data]
        } else {
          var response = await HTTP.get(catlgType + '/?ids='+ id.join(','))
          var catlgItemFetch = response.data   
        }
          
        await dispatch('FETCHdependentCatlg', catlgItemFetch)

        catlgItemFetch.forEach(function(item, i, arr){
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            dispatch('SETcatlgLabel', [catlgType, item.id])
          }
        })
      } catch(error) {
        console.log(error)
      }

    },

    FETCHcatlg: async ({commit, dispatch, getters}, [catlgType, query, fields]) => {
      try {
        if ((query == undefined) | (fields == undefined)) {
          var response = await HTTP.get(catlgType + '/')
        } else {
          var response = await HTTP.get(`${catlgType}/?query=${query}&fields=${fields.join(',')}`)
        }
        var catlgItemFetch = response.data

        await dispatch('FETCHdependentCatlg', catlgItemFetch)      
        catlgItemFetch.forEach(function(item, i, arr){
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            dispatch('SETcatlgLabel', [catlgType, item.id])
          }    
        })
      } catch(error) {
        console.log(error)
      }
    },

    FETCHdependentCatlg: async ({commit, dispatch, getters}, items) => {
      for (var key in items[0]){
        if (getters.catlgExist(key)) {
          var catlgToLoad = _.uniq(_.map(items, _.property(key)))
          catlgToLoad = catlgToLoad.filter(function (el) {
            return el != null;
          });
          //console.log(catlgToLoad)
          await dispatch('FETCHcatlgItem', [key, catlgToLoad])
        }
      }
    },

    SETcatlgLabel: ({commit, dispatch, getters}, [catlgType, id]) => {
      var label = "unknown";
      if (isNaN(id)){
        var catlgItem = id; //не число, значит передан объект
      } else {
        var catlgItem = getters.GETcatlgItem(catlgType, id); //число, значит передано id
      }
      switch(catlgType){
        case 'device':
          var deviceType = getters.GETcatlgItem('deviceType', catlgItem.deviceType).label
          var nomenclature = getters.GETcatlgItem('nomenclature', catlgItem.nomenclature).label
          var serial_num = catlgItem['serial_num'] 
          label = deviceType + ' ' + nomenclature + ' (' + serial_num + ')';
          break;

        case 'person':
          label = catlgItem['surname'] + ' ' + catlgItem['name'];
          break;
      }
      commit('SETcatlgItemLabel', [catlgType, id, label])
    },

  
  },

});