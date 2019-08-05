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

    catlgExist: (state, catlgType) => {
      if (catlgType in state.catlgs) {
        return true
      } else {
        return false
      }
    },

    GETcatlgItem: (state, catlgType, id) => {
      if (state.catlgs.catlgType.id) {
        return state.catlgs.catlgType.id
      } else {
        return null
      }
    },


  },
  mutations: {
    SETcurrentDoc: (state, data) => {
      state.currentDoc.data = data
    },

    SETcatlgItem: (state, catlgType, item) => {
      state.catlgs[catlgType][item.id] = item
    },

    SETcatlgLabel: (state, catlgType, id) => {
      var label = "unknown";
      if (isNaN(id)){
        var catlgItem = id; //не число, значит передан объект
      } else {
        var catlgItem = vm.catlgs[catlgName][id]; //число, значит передано id
      }
      switch(catlgName){
        case 'device':
          var deviceType = vm.catlgs['deviceType'][catlgItem.deviceType]['label'];
          var nomenclature = vm.catlgs['nomenclature'][catlgItem.nomenclature]['label'];
          var serial_num = catlgItem['serial_num'] 
          label = deviceType + ' ' + nomenclature + ' (' + serial_num + ')';
          break;

        case 'person':
          label = catlgItem['surname'] + ' ' + catlgItem['name'];
          break;
      }
      Vue.set(vm.catlgs[catlgName][id], 'label', label)
    },

  },
  actions: {
    FETCHcurrentDoc: async (context, docType, id) => {
      let response = await HTTP.get(docType + '/' + id + '/')
      //vm.fetchWidgetInitCatlg(response.data['table_unit'], {'device': 'device', 'person': 'person'})
      context.commit('SETcurrentDoc', response.data)

      for (let key in response.data){
        if ((context.getters.catlgExist(key)) && (response.data[key])) {
          context.dispatch('FETCHcatlgItem', key, response.data[key])
        }
      }
    },

    FETCHcatlgItem: async (context, catlgType, id) => {
      try {
        if (!Array.isArray(id)){
          var response = await HTTP.get(catlgType + '/'+ id + '/')
          var catlgItemFetch = [response.data]
        } else {
          var response = await HTTP.get(catlgType + '/?ids='+ id.join(','))
          var catlgItemFetch = response.data   
        }
          
        await context.dispatch('FETCHdependentCatlg', catlgItemFetch)

        catlgItemFetch.forEach(function(item, i, arr){
          context.commit('SETcatlgItem', catlgType, item)
          if ( !('label' in item)) {
            vm.setCatlgLabel(catlgType, item.id)
          }
        })
      } catch(error) {
        console.log(error)
      }

    },

    FETCHdependentCatlg: async (context, items) => {
      for (var key in items[0]){
        if (context.getters.catlgExist(key)) {
          var catlgToLoad = _.uniq(_.map(items, _.property(key)))
          catlgToLoad = catlgToLoad.filter(function (el) {
            return el != null;
          });
          //console.log(catlgToLoad)
          await context.dispatch('FETCHcatlgItem', key, catlgToLoad)
        }
      }
    },


  },
});