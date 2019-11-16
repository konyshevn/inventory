import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
import {HTTP} from '../../http-common'
var _ = require('lodash');
import * as DocConstructor from '@/components/Doc/common/doc-constructor.js'

async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

export const store = new Vuex.Store({
  state: {
    currentDoc: {
      data: {},
      status: {
        docType: String,
        tableUnit: {
          sort: {field: "", fieldType: "", order: -1},
          selected: []
        },
        loading: true,
      }
    },
    
    widgetIsValid: [],
    
    docs: {
      data: [],
      filtered: [],
      status: {
        sort: {field: "doc_date", fieldType: "text", order: -1},
        selected: [],
      }
    },
    catlgs: {
      department: {
        data: [],
        status: {
          sort: {field: "label", fieldType: "text", order: 1},
          selected: [],
        },
      },
      stock: {
        data: [],
        status: {
          sort: {field: "label", fieldType: "text", order: 1},
          selected: [],
        },
      },
      person: {
        data: [],
        status: {
          sort: {field: "surname", fieldType: "text", order: 1},
          selected: [],
        },
      },
      device: {
        data: [],
        status: {
          sort: {field: "deviceType", fieldType: "widget", order: 1},
          selected: [],
        },
      },
      deviceType: {
        data: [],
        status: {
          sort: {field: "label", fieldType: "text", order: 1},
          selected: [],
        },
      },
      nomenclature: {
        data: [],
        status: {
          sort: {field: "label", fieldType: "text", order: 1},
          selected: [],
        },
      },
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

    widgetsIsValid: state => parent => {
      let result = true
      let widgets = _.filter(state.widgetIsValid, {parent: parent})
      widgets.forEach(function(item){
        result = result && item.isValid
      })
      return result
    },

    GETcatlgItem: state => (catlgType, id) => {
      let catlgItem = _.find(state.catlgs[catlgType]['data'], {id: Number(id)})
      return catlgItem
    },

    GETcatlgItemLabel: state => (catlgType, id) => {
      let catlgItem = _.find(state.catlgs[catlgType]['data'], {id: id})
      if (catlgItem != null){
        return catlgItem.label
      }
    },

    GETcatlg: state => catlgType => {
      return state.catlgs[catlgType]['data']
    },

    GETcatlgByLabel: state => (catlgType, label) => {
      let catlg = _.filter(state.catlgs[catlgType]['data'], function(item) { 
        return item['label'].toLowerCase().indexOf(label.toLowerCase()) != -1
      })
      return catlg
    },

    GETdocs: state => {
      return state.docs.data
    },

    GETsortStatus: state => objType => {
      var status
      if (objType == "TU") {
        status = state.currentDoc.status.tableUnit.sort
      } else if (objType == "docs") {
        status = state.docs.status.sort
      } else if ('catlg' in objType) {
        status = state.catlgs[objType.catlg].status.sort
      }
      return status
    }


  },
  mutations: {
    SETcurrentDoc: (state, data) => {
      state.currentDoc.data = data
    },

    DELcurrentDoc: (state) => {
      state.currentDoc.data = {}
      state.currentDoc.status = {
        docType: String,
        tableUnit: {
          sort: {field: "", fieldType: "", order: -1},
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


    SETwidgetState: (state, [parent, uid, isValid]) => {
      let uidIndex = _.findIndex(state.widgetIsValid, {uid: uid})
      if (uidIndex >= 0) {
        state.widgetIsValid.splice(uidIndex, 1)
      }
      state.widgetIsValid.push({parent: parent, uid: uid, isValid: isValid})
    },

    DELwidgetState: (state, uid) => {
      let uidIndex = _.findIndex(state.widgetIsValid, {uid: uid})
      if (uidIndex >= 0) {
        state.widgetIsValid.splice(uidIndex, 1)
      }
    },


    UPDcurrentDocTU: (state, [index, key, value]) => {
      state.currentDoc.data.table_unit[index][key] = value
    },

    DELcurrentDocTUrow: (state) => {
      let rowToDelete = state.currentDoc.status.tableUnit.selected
      state.currentDoc.data.table_unit.forEach(function(item){
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
      var catlgItemIndex = _.findIndex(state.catlgs[catlgType]['data'], {id: item.id})
      if (catlgItemIndex >= 0) {
        state.catlgs[catlgType]['data'][catlgItemIndex] = item
      } else {
        state.catlgs[catlgType]['data'].push(item)
      }
    },

    SETcatlgItemLabel: (state, [catlgType, id, label]) => {
      let catlgItemIndex = _.findIndex(state.catlgs[catlgType]['data'], {id: id})
      if (catlgItemIndex >= 0) {
        state.catlgs[catlgType]['data'][catlgItemIndex]['label'] = label
      }
    },


    sortObjList: (state, [objType, field, fieldType, changeOrder = true]) => {
      var status, data 
      if (objType == "TU") {
        status = state.currentDoc.status.tableUnit.sort
        data = state.currentDoc.data.table_unit
      } else if (objType == "docs") {
        status = state.docs.status.sort
        data = state.docs.data
      } else if ('catlg' in objType) {
        status = state.catlgs[objType.catlg].status.sort
        data = state.catlgs[objType.catlg].data
      }

      if (status.field != field) {
        status.order = -1
      }
      if (changeOrder) {
        status.order *= -1
      }
      status.field = field
      status.fieldType = fieldType
      var order = status.order

      function compareTUrowWidget(a, b) {
        if (!a[field]) return 1;
        if (!b[field]) return -1;

        
        let catlgItemA = _.find(state.catlgs[field]['data'], {id: a[field]})
        let catlgItemB = _.find(state.catlgs[field]['data'], {id: b[field]})
        var aLabel = catlgItemA.label
        var bLabel = catlgItemB.label
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
        data.sort(compareTUrowWidget);
      } else if (fieldType == 'number') {
        data.sort(compareTUrowNumber);
      } else if (fieldType == 'text') {
        data.sort(compareTUrowText);
      }

      if (objType == "TU") {
        data.map(function(value, index){
          value.rowOrder = index + 1
        })
      }
    },

    DELcatlgItem: (state, [catlgType, id]) => {
      let catlgItemIndex = _.findIndex(state.catlgs[catlgType]['data'], {id: id})
      if (catlgItemIndex >= 0) {
        state.catlgs[catlgType]['data'].splice(catlgItemIndex, 1)
      }
    },

    currentDocTUclearNullId: (state) => {
      state.currentDoc.data.table_unit.forEach(function(item){
        if (String(item.id).indexOf("null_") == 0) {
          item.id = null
        }
      })
    },

  },

  actions: {
    PUTcurrentDoc: async ({dispatch, getters}) => {
      var response = null
      try {
        var currentDoc = getters.currentDoc
        if (currentDoc.doc_num == "") {
          currentDoc.doc_num = null
        }

        currentDoc.table_unit.forEach(function(item){
          if (String(item.id).indexOf("null_") == 0) {
            item.id = null
          }
        })

        if (currentDoc.id == null) {
          response = await HTTP.post(getters.currentDocStatus.docType + '/', currentDoc)
        } else {
          response = await HTTP.put(getters.currentDocStatus.docType + '/' + getters.currentDoc.id + '/', currentDoc)
        }

        if (response.status >= 200 && response.status < 300) {
          dispatch('FETCHcurrentDoc', [getters.currentDocStatus.docType, response.data.id])
        }
      } catch(error) {
        response = error['response']
      } 
      return response

    },

    PUTcatlg: async({commit, dispatch, getters}, [catlgType, item]) => {
      var response = null
      try {
        if (item.id == null) {
          response = await HTTP.post(catlgType + '/', item)
        } else {
          response = await HTTP.put(catlgType + '/' + item.id + '/', item)
        }
        if (response.status >= 200 && response.status < 300) {
          item = response.data
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            dispatch('SETcatlgLabel', [catlgType, item.id])
          }
          let sortStatus = getters.GETsortStatus({catlg: catlgType})
          commit('sortObjList', [{catlg: catlgType}, sortStatus.field, sortStatus.fieldType, false])
        }

      } catch(error) {
        response = error['response']
      } 
      return response
    },

    DELcurrentDoc: async ({getters}) => {
      var response = null
      try{
        response = await HTTP.delete(getters.currentDocStatus.docType + '/' + getters.currentDoc.id + '/')
      } catch(error) {
        response = error['response']
      } 
      return response

    },

    DELdoc: async ({dispatch}, [docType, id]) => {
      var response = null
      try {
        response = await HTTP.delete(docType + '/' + id + '/')
        if (response.status == 204) {
          dispatch('FETCHdocs', docType)
        }
      } catch (error) {
        response = error['response']
      }
      return response
    },

    DELcatlg: async ({commit}, [catlgType, id]) => {
      var response = null
      try{
        response = await HTTP.delete(catlgType + '/' + id + '/')
        if (response.status == 204) {
          commit('DELcatlgItem', [catlgType, id])
        }
      } catch(error) {
        response = error['response']
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
      /*
      let sortStatus = getters.GETsortStatus('docs')
      function compareTUrowText(a, b) {
        if(a[sortStatus.field] === "" || a[sortStatus.field] === null) return 1;
        if(b[sortStatus.field] === "" || b[sortStatus.field] === null) return -1;
        if(a[sortStatus.field] === b[sortStatus.field]) return 0;
        return a[sortStatus.field] < b[sortStatus.field] ? -1 * sortStatus.order : 1 * sortStatus.order;
      }
      */
      let response = await HTTP.get(docType + '/')
      let DocsReady = response.data
      //DocsReady.sort(compareTUrowText)
      commit('SETdocs', DocsReady)
      await dispatch('FETCHdependentCatlg', DocsReady)
      let sortStatus = getters.GETsortStatus('docs')
      commit('sortObjList', ['docs', sortStatus.field, sortStatus.fieldType, false])
    },

    FETCHwidgetInitCatlg: async ({dispatch}, [tableUnit, fieldsMap]) => {
      for (var fieldTableUnit in fieldsMap) {
        var catlgType  = fieldsMap[fieldTableUnit]
        var catlgToLoad = _.uniq(_.map(tableUnit, _.property(fieldTableUnit)))
        catlgToLoad = catlgToLoad.filter(function (el) {
            return el != null;
          });
         await dispatch('FETCHcatlgItem', [catlgType, catlgToLoad])
      }
    },

    FETCHcatlgItem: async ({commit, dispatch}, [catlgType, id]) => {
      var response = null
      var catlgItemFetch = []
      try {
        if (!Array.isArray(id)){
          response = await HTTP.get(catlgType + '/'+ id + '/')
          catlgItemFetch = [response.data]
        } else {
          response = await HTTP.get(catlgType + '/?ids='+ id.join(','))
          catlgItemFetch = response.data   
        }
          
        await dispatch('FETCHdependentCatlg', catlgItemFetch)

        //catlgItemFetch.forEach(function(item){
        await asyncForEach(catlgItemFetch, async function(item){
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            await dispatch('SETcatlgLabel', [catlgType, item.id])
          }
        })
      } catch(error) {
        response = error['response']
      }
      return response
    },

    FETCHcatlg: async ({commit, dispatch, getters}, [catlgType, query, fields]) => {
      var response = null
      try {
        if ((query == undefined) | (fields == undefined)) {
          response = await HTTP.get(catlgType + '/')
        } else {
          response = await HTTP.get(`${catlgType}/?query=${query}&fields=${fields.join(',')}`)
        }
        var catlgItemFetch = response.data

        await dispatch('FETCHdependentCatlg', catlgItemFetch)      
        //catlgItemFetch.forEach(function(item){
        await asyncForEach(catlgItemFetch, async function(item){
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            await dispatch('SETcatlgLabel', [catlgType, item.id])
          }    
        })
        let sortStatus = getters.GETsortStatus({catlg: catlgType})
        commit('sortObjList', [{catlg: catlgType}, sortStatus.field, sortStatus.fieldType, false])
      } catch(error) {
        response = error['response']
      } 
      return response
    },

    FETCHdependentCatlg: async ({dispatch, getters}, items) => {
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

    SETcatlgLabel: ({commit, getters}, [catlgType, id]) => {
      var label = "unknown";
      var catlgItem = null
      if (isNaN(id)){
        catlgItem = id; //не число, значит передан объект
      } else {
        catlgItem = getters.GETcatlgItem(catlgType, id); //число, значит передано id
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