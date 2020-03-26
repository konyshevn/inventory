import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
import {HTTP} from '../../http-common'
var _ = require('lodash');
import {aliases} from '@/components/common/aliases.js';

async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

//import * as DocConstructor from '@/components/Doc/common/doc-constructor.js'
/* eslint-disable no-console */
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
      docincome: {
        data: [],
        status: {
          sort: {field: "doc_date", sortAsc: true},
        }
      },
      docmove: {
        data: [],
        status: {
          sort: {field: "doc_date", sortAsc: true},
        }
      },
     docwriteoff: {
        data: [],
        status: {
          sort: {field: "doc_date", sortAsc: true},
        }
      },
      docinventory: {
        data: [],
        status: {
          sort: {field: "doc_date", sortAsc: true},
        }
      },
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
//---------------------------Document---------------------------
    GETdocItem: state => (docType, id) => {
      let docItem = _.find(state.docs[docType]['data'], {id: Number(id)})
      return docItem
    },

    GETdocs: state => docType => {
      return state.docs[docType]['data']
    },


//---------------------------Catalog---------------------------
    catlgExist: state => catlgType => {
      if (catlgType in state.catlgs) {
        return true
      } else {
        return false
      }
    },

    GETcatlgItem: state => (catlgType, id) => {
      let catlgItem = _.find(state.catlgs[catlgType]['data'], {id: Number(id)})
      return catlgItem
    },

    GETcatlgItemLabel: state => (catlgType, id) => {
      let catlgItem = _.find(state.catlgs[catlgType]['data'], {id: id})
      let label = ''
      if (catlgItem != null){
        label = catlgItem.label
      } 
      return label
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

//---------------------------Widget---------------------------
    widgetsIsValid: state => parent => {
      let result = true
      let widgets = _.filter(state.widgetIsValid, {parent: parent})
      widgets.forEach(function(item){
        result = result && item.isValid
      })
      return result
    },

  },

  mutations: {
//---------------------------Document---------------------------
    SETdocs: (state, [docType, data]) => {
      state.docs[docType]['data'] = data
    },

    SETdocItem: (state, [docType, item]) => {
      var docItemIndex = _.findIndex(state.docs[docType]['data'], {id: item.id})
      if (docItemIndex >= 0) {
        state.docs[docType]['data'][docItemIndex] = item
      } else {
        state.docs[docType]['data'].push(item)
      }
    },

    DELdocItem: (state, [docType, id]) => {
      let docItemIndex = _.findIndex(state.docs[docType]['data'], {id: id})
      if (docItemIndex >= 0) {
        state.docs[docType]['data'].splice(docItemIndex, 1)
      }
    },
//---------------------------Catalog---------------------------
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

    DELcatlgItem: (state, [catlgType, id]) => {
      let catlgItemIndex = _.findIndex(state.catlgs[catlgType]['data'], {id: id})
      if (catlgItemIndex >= 0) {
        state.catlgs[catlgType]['data'].splice(catlgItemIndex, 1)
      }
    },


//---------------------------Widget---------------------------
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
  
  },

  actions: {
//---------------------------Document---------------------------
    PUTdoc: async ({commit}, [docType, item]) => {
      var response = null
      try {
        var currentDoc = item
        if (currentDoc.doc_num == "") {
          currentDoc.doc_num = null
        }
        currentDoc.table_unit.forEach(function(item, index){
          if (String(item.id).indexOf("null_") == 0) {
            item.id = null
          }
          item.rowOrder = index + 1 
        })

        if (currentDoc.id == null) {
          response = await HTTP.post(docType + '/', currentDoc)
        } else {
          response = await HTTP.put(docType + '/' + currentDoc.id + '/', currentDoc)
        }

        if (response.status >= 200 && response.status < 300) {
          item = response.data
          commit('SETdocItem', [docType, item])
          //dispatch('FETCHcurrentDoc', [getters.currentDocStatus.docType, response.data.id])
        }
      } catch(error) {
        response = error['response']
      } 
      return response
    },

    DELdoc: async ({commit}, [docType, id]) => {
      var response = null
      try {
        response = await HTTP.delete(docType + '/' + id + '/')
        if (response.status >= 200 && response.status < 300) {
          commit('DELdocItem', [docType, id])
        }
      } catch (error) {
        response = error['response']
      }
      return response
    },

    FETCHdocs: async ({commit, dispatch}, [docType, id]) => {

        if (id){
          response = await HTTP.get(docType + '/?ids='+ id.join(','))
        } else {
          response = await HTTP.get(docType + '/')
        }



      let response = await HTTP.get(docType + '/')
      let DocsReady = response.data




      // console.log('FETCHdocs: aliases', aliases.docAlias[docType]['fieldsMap'])
      await dispatch('FETCHdependentCatlg', [DocsReady, aliases.docAlias[docType]['fieldsMap']])
      commit('SETdocs', [docType, DocsReady])
    },

    FETCHdocItem: async ({commit, dispatch}, [docType, id]) => {
      if (docType && id) {

        let response = await HTTP.get(docType + '/' + id + '/')

      /*
      await dispatch('FETCHwidgetInitCatlg', [response.data['table_unit'], aliases.docAlias[docType].fieldsMap])

      for (let key in response.data){
        if ((getters.catlgExist(key)) && (response.data[key])) {
          await dispatch('FETCHcatlgItem', [key, response.data[key]])
        }
      }
      */
        await dispatch('FETCHdependentCatlg', [[response.data], aliases.docAlias[docType].fieldsMap])
        await dispatch('FETCHdependentCatlg', [response.data.table_unit, aliases.docAlias[docType].fieldsMap.tableUnit])

        commit('SETdocItem', [docType, response.data])
      }
    },

    FETCHdocItemExtra: async ({dispatch}, [docType, id, extra]) => {
      let response = await HTTP.get(docType + '/' + id + '/' + extra + '/')
      await dispatch('FETCHdependentCatlg', [response.data, aliases.docAlias[docType].fieldsMap.tableUnit])
      return response.data
    },

    docFollower: async ({dispatch}, [docType, id]) => {
      let response = await HTTP.get(docType + '/' + id + '/get_follower/')
      let followers = response.data
      asyncForEach(followers, async function(follower){
        await dispatch('FETCHdocItem', [follower.docType, follower.docId])
      })
      return followers
    },

    docLeader: async ({dispatch}, [docType, id]) => {
      let response = await HTTP.get(docType + '/' + id + '/get_leader/')
      // console.log('docLeader: response', response)
      let leader = response.data
      await dispatch('FETCHdocItem', [leader.docType, leader.docId])
      return leader
    },

    CREATEdocFollower: async (context, [docType, id, followerType]) => {
      let response = await HTTP.get(docType + '/' + id + '/create_follower/?follower_type=' + followerType)
      return response.data
    },


//---------------------------Catalog---------------------------
    PUTcatlg: async({commit, dispatch}, [catlgType, item]) => {
      var response = null
      try {
        if (item.id == null) {
          response = await HTTP.post(catlgType + '/', item)
        } else {
          response = await HTTP.put(catlgType + '/' + item.id + '/', item)
        }
        // console.log('PUTcatlg: response', response)
        if (response.status >= 200 && response.status < 300) {
          item = response.data
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            dispatch('SETcatlgLabel', [catlgType, item.id])
          }
          // let sortStatus = getters.GETsortStatus({catlg: catlgType})
          // commit('sortObjList', [{catlg: catlgType}, sortStatus.field, sortStatus.fieldType, false])
        }

      } catch(error) {
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
          
        await dispatch('FETCHdependentCatlg', [catlgItemFetch, aliases.catlgAlias[catlgType]['fieldsMap']])

        catlgItemFetch.forEach(function(item){
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            dispatch('SETcatlgLabel', [catlgType, item.id])
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

        await dispatch('FETCHdependentCatlg', [catlgItemFetch, aliases.catlgAlias[catlgType]['fieldsMap']])      
        catlgItemFetch.forEach(function(item){
          commit('SETcatlgItem', [catlgType, item])
          if ( !('label' in item)) {
            dispatch('SETcatlgLabel', [catlgType, item.id])
          }    
        })
        let sortStatus = getters.GETsortStatus({catlg: catlgType})
        commit('sortObjList', [{catlg: catlgType}, sortStatus.field, sortStatus.fieldType, false])
      } catch(error) {
        response = error['response']
      } 
      return response
    },

    FETCHdependentCatlg: async ({dispatch, getters}, [items, fieldsMap]) => {
      let key
      // console.log('FETCHdependentCatlg: items', items)
      // console.log('FETCHdependentCatlg: fieldsMap', fieldsMap)
      for (var itemKey in items[0]){
        if (fieldsMap && (itemKey in fieldsMap)) {
          key = fieldsMap[itemKey]
        } else {
          key = itemKey
        }
        if (getters.catlgExist(key)) {
          var catlgToLoad = _.uniq(_.map(items, _.property(itemKey)))
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

//---------------------------Widget---------------------------
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

//---------------------------Report---------------------------
    FETCHreportOptions: async (context, reportName) => {
      var response = null
      try {
        response = await HTTP.get('/report/' + reportName + '/')
      } catch(error) {
        response = error['response']
      } 
      return response
    },

    FETCHreport: async ({dispatch}, [reportName, filterReq]) => {
      var response = null
      var fieldsMap = {}
      var docsFields = []
      var docsToLoad = {}

      try {
        response = await HTTP.post('/report/' + reportName + '/', {filter_req: filterReq})
        let reportData = response.data
        var reportOptions = await dispatch('FETCHreportOptions', reportName)
        var fields_options = reportOptions.data[0]['fields_options']
        
        for (let field in fields_options) {
          if (typeof fields_options[field]['type'] === 'object' && fields_options[field]['type'] !== null && 'catlg' in fields_options[field]['type']) {
            fieldsMap[field] = fields_options[field]['type']['catlg']
          } else if (fields_options[field]['type'] == 'doc') {
            docsFields.push(field)
          } 
        }

        await dispatch('FETCHdependentCatlg', [reportData, fieldsMap])

        reportData.forEach(function(item){
          docsFields.forEach(function(field) {
            if (!(item[field]['docType'] in docsToLoad)) {
              docsToLoad[item[field]['docType']] = []
            }
            if (!(item[field]['docId'] in docsToLoad[item[field]['docType']])) {
              docsToLoad[item[field]['docType']].push(item[field]['docId'])
            }
          })
        })

        for (let docType in docsToLoad) {
          await dispatch('FETCHdocs', [docType, docsToLoad[docType]])    
        }     

      } catch(error) {
        response = error['response']
      } 
      return response
    },
 
  },

});