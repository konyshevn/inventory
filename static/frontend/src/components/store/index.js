import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
import {HTTP} from '../../http-common'
var _ = require('lodash');
import * as DocConstructor from '../doc-constructor.js'

export const store = new Vuex.Store({
  state: {
    currentDoc: {
      data: {},
      status: {
        docType: String,
        widgetIsValid: {},
        tableUnit: {
          sort: {field: "", order: -1},
          selected: []
        },
        loading: true,
      }
    },
    docs: {
      data: [],
      status: {
        selected: [],
      }
    },
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

    currentDocTU: state => {
      return state.currentDoc.data.table_unit
    },

    currentDocStatus: state => {
      return state.currentDoc.status
    },

    currentDocStatusTableUnit: state => key => {
      return state.currentDoc.status.tableUnit[key]
    },

    catlgExist: state => catlgType => {
      if (catlgType in state.catlgs) {
        return true
      } else {
        return false
      }
    },

    widgetsIsValid: state => {
      var result = true
      for (let uid in state.currentDoc.status.widgetIsValid) {
        console.log('widgetIsValid: uid, state', uid, state.currentDoc.status.widgetIsValid[uid])
        result = result && state.currentDoc.status.widgetIsValid[uid]
      }
      console.log('widgetIsValid: result', result)
      return result
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
      return state.docs.data
    },


  },
  mutations: {
    SETcurrentDoc: (state, data) => {
      state.currentDoc.data = data
    },

    DELcurrentDoc: (state) => {
      state.currentDoc.data = {}
      state.currentDoc.status = {
        docType: String,
        widgetIsValid: {},
        tableUnit: {
          sort: {field: "", order: -1},
          selected: []
        },
        loading: true,
      }
    },

    INITcurrentDoc: (state, docType) => {
      let newDoc = new DocConstructor[docType]
      Vue.set(state.currentDoc.status, 'docType', docType)
      Vue.set(state.currentDoc, 'data', newDoc)
    },

    SETcurrentDocType: (state, data) => {
      state.currentDoc.status.docType = data
    },


    SETcurrentDocWidgetState: (state, [uid, isValid]) => {
      Vue.set(state.currentDoc.status.widgetIsValid, uid, isValid)
    },

    DELcurrentDocWidgetState: (state, uid) => {
      Vue.delete(state.currentDoc.status.widgetIsValid, uid)
    },

    UPDcurrentDocTU: (state, [index, key, value]) => {
      state.currentDoc.data.table_unit[index][key] = value
    },

    DELcurrentDocTUrow: (state) => {
      let rowToDelete = state.currentDoc.status.tableUnit.selected
      state.currentDoc.data.table_unit.forEach(function(item, i, arr){
        if ((rowToDelete.indexOf(item.id) >= 0) || (rowToDelete.indexOf(String(item.id)) >= 0)) {
          item.DELETE = true
        } 
      })
      state.currentDoc.status.tableUnit.selected = []
    },
    
    ADDcurrentDocTUrow: (state) => {
      let newDoc = new DocConstructor[state.currentDoc.status.docType]
      state.currentDoc.data.table_unit.push(newDoc.table_unit[0])
    },

    UPDcurrentDoc: (state, [key, value]) => {
      if (value instanceof Event) {
        state.currentDoc.data[key] = value.data
      } else {
        state.currentDoc.data[key] = value
      }
    },

    UPDcurrentDocTableUnitSelected: (state, event) => {
      if (event.target.checked) {
        state.currentDoc.status.tableUnit.selected.push(event.target.value)
      } else {
        state.currentDoc.status.tableUnit.selected = state.currentDoc.status.tableUnit.selected.filter(item => {
          return item != event.target.value
        })
      }
    },

    UPDdocsSelected: (state, event) => {
      if (event.target.checked) {
        state.docs.status.selected.push(event.target.value)
      } else {
        state.docs.status.selected = state.docs.status.selected.filter(item => {
          return item != event.target.value
        })
      }
    },

    SETdocs: (state, data) => {
      state.docs.data = data
    },

    SETcatlgItem: (state, [catlgType, item]) => {
      Vue.set(state.catlgs[catlgType], item.id, item)
    },

    SETcatlgItemLabel: (state, [catlgType, id, label]) => {
      Vue.set(state.catlgs[catlgType][id], 'label', label)
    },

    sortTU: (state, [field, fieldType]) => {
      if (state.currentDoc.status.tableUnit.sort.field != field) {
        state.currentDoc.status.tableUnit.sort.order = -1
      }
      state.currentDoc.status.tableUnit.sort.order *= -1
      state.currentDoc.status.tableUnit.sort.field = field
      var order = state.currentDoc.status.tableUnit.sort.order

      function compareTUrowWidget(a, b) {
        if (!a[field]) return 1;
        if (!b[field]) return -1;

        var aLabel = state.catlgs[field][a[field]]['label']
        var bLabel = state.catlgs[field][b[field]]['label']
        return aLabel < bLabel ? -1 * order : 1 * order;
      }

      function compareTUrowNumber(a, b) {
        return Number(a[field]) < Number(b[field]) ? -1 * order : 1 * order;
      }

      function compareTUrowText(a, b) {
        if(a[field] === "" || a[field] === null) return 1;
        if(b[field] === "" || b[field] === null) return -1;
        if(a[field] === b[field]) return 0;
        return a[field] < b[field] ? -1 * order : 1 * order;
      }

      if (fieldType == 'widget') {
        state.currentDoc.data.table_unit.sort(compareTUrowWidget);
      } else if (fieldType == 'number') {
        state.currentDoc.data.table_unit.sort(compareTUrowNumber);
      } else if (fieldType == 'text') {
        state.currentDoc.data.table_unit.sort(compareTUrowText);
      }

      state.currentDoc.data.table_unit.map(function(value, index){
        value.rowOrder = index + 1
      })
    },

    currentDocTUclearNullId: (state) => {
      state.currentDoc.data.table_unit.forEach(function(item, i, arr){
        if (String(item.id).indexOf("null_") == 0) {
          item.id = null
        }
      })
    },

  },

  actions: {
    PUTcurrentDoc: async ({commit, dispatch, getters}) => {
      //commit('currentDocTUclearNullId')
      var currentDoc = getters.currentDoc

      currentDoc.table_unit.forEach(function(item, i, arr){
        if (String(item.id).indexOf("null_") == 0) {
          item.id = null
        }
      })

      if (currentDoc.id == null) {
        var response = await HTTP.post(getters.currentDocStatus.docType + '/', currentDoc)
      } else {
        var response = await HTTP.put(getters.currentDocStatus.docType + '/' + getters.currentDoc.id + '/', currentDoc)
      }

      console.log('PUTcurrentDoc: response', response.status, response.statusText, response.data, )
      if (response.status == 200 || response.status == 201) {
        dispatch('FETCHcurrentDoc', [getters.currentDocStatus.docType, response.data.id])
      }
      return response
    },

    DELcurrentDoc: async ({commit, dispatch, getters}) => {
      let response = HTTP.delete(getters.currentDocStatus.docType + '/' + getters.currentDoc.id + '/')
      return response
    },

    DELdoc: async ({commit, dispatch, getters}, [docType, id]) => {
      let response = await HTTP.delete(docType + '/' + id + '/')
      if (response.status == 204) {
        dispatch('FETCHdocs', docType)
      }
      return response
    },

    FETCHcurrentDoc: async ({commit, dispatch, getters}, [docType, id]) => {
      let response = await HTTP.get(docType + '/' + id + '/')
      await dispatch('FETCHwidgetInitCatlg', [response.data['table_unit'], {device: 'device', person: 'person'}])

      for (let key in response.data){
        if ((getters.catlgExist(key)) && (response.data[key])) {
          await dispatch('FETCHcatlgItem', [key, response.data[key]])
        }
      }
      commit('SETcurrentDoc', response.data)
      commit('SETcurrentDocType', docType)
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
         await dispatch('FETCHcatlgItem', [catlgType, catlgToLoad])
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