<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
import CatlgCommon from './CatlgCommon.vue';
import Common from './Common.vue';
var _ = require('lodash');
import {EventBus} from './event-bus.js'
import moment from 'moment';
import * as DocConstructor from './doc-constructor.js'

export default {
  name: 'DocCommon',
  mixins: [Common, CatlgCommon],
  props: {
    //msg: String
  },
  data () {
    return {
      doc: {},
      docs: [],
      widgetIsValid: {},
      tableUnit:{
        sort:{
          field: "",
          order: -1,
        }
      }
    }
  },

  methods: {
    fetchDocs: function (docType) {
      var vm = this;
      HTTP.get(docType + '/')
        .then(function (response) {
          var DocsReady = response.data
          vm.docs = DocsReady
          for (var key in DocsReady[0]){
            if (key in vm.catlgs) {
              var catlgToLoad = _.uniq(_.map(DocsReady, _.property(key)))
              catlgToLoad = catlgToLoad.filter(function (el) {
                return el != null;
              });

              vm.fetchCatlgItem(key, catlgToLoad)
            }
          }
        })
    },

    async getDocItem (docType, id) {
      var vm = this;
      var response = await HTTP.get(docType + '/' + id + '/')
      vm.fetchWidgetInitCatlg(response.data['table_unit'], {'device': 'device', 'person': 'person'})
      vm.doc = response.data;
      for (var key in vm.doc){
        if ((key in vm.catlgs) && (vm.doc[key])) {
          vm.fetchCatlgItem(key, vm.doc[key])
        }
      }

    },

    getErrorMsg: function(error) {
      var errorMsg = ''
      if (error.response) {
        if (error.response.data) {
          errorMsg = errorMsg + error.response.data
        }
      } else if (error.message) {
        errorMsg = errorMsg + error.message
      }
      return errorMsg
    },

    sortTU: function(TU, field, fieldType){
      var vm = this
      if (vm.tableUnit.sort.field != field) {
        vm.tableUnit.sort.order = -1
      }
      vm.tableUnit.sort.order *= -1
      vm.tableUnit.sort.field = field
      var order = vm.tableUnit.sort.order

      function compareTUrowWidget(a, b) {
        var aLabel = vm.catlgs[field][a[field]]['label']
        var bLabel = vm.catlgs[field][b[field]]['label']
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
        TU.sort(compareTUrowWidget);
      } else if (fieldType == 'number') {
        TU.sort(compareTUrowNumber);
      } else if (fieldType == 'text') {
        TU.sort(compareTUrowText);
      }

      TU.map(function(value, index){
        value.rowOrder = index + 1
      })

    },

    async regWriteDocItem (docType, item) {
      var vm = this;
      var itemStatus = item.active
      item.active = true
      try {
        if (!vm.isValid()) { 
          throw new Error('Заполните все необходимые реквизиты документа.')
        }
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
        
        //vm.$bvModal.show('status-msg')
      } catch(error) {
        item.active = itemStatus
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка проведения: ${vm.getErrorMsg(error)}`])
      }
    },

    async regDelDocItem (docType, item) {
      var vm = this;
      var itemStatus = item.active
      item.active = false
      try {
        if (!vm.isValid()) { 
          throw new Error('Заполните все необходимые реквизиты документа.')
        }
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
      } catch(error) {
        item.active = itemStatus
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка отмены проведения: ${vm.getErrorMsg(error)}`])
      }
    },

    async saveDocItem (docType, item) {
      var vm = this;
      try {
        if (!vm.isValid()) { 
          throw new Error('Заполните все необходимые реквизиты документа.')
        }
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
      } catch(error) {
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка сохранения: ${vm.getErrorMsg(error)}`])
      }
    },

    async delDocItem (docType, item) {
      var vm = this;
      var status = true
      try {
        var confirm = await vm.confirmMsg('Вы действительно хотите удалить документ?')
        if (confirm) {
          var response = await HTTP.delete(docType + '/' + item.id + '/')
        } else {
          status = false
        }
      } catch(error) {
        status = false
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка удаления: ${vm.getErrorMsg(error)}`])
      } finally {
        if (status) {
          vm.$router.push({ name: 'doc.list', params: {docType: docType} })
        }
      }
    },

    addRowTableUnit: function(docType, doc) {
      var vm = this
      var newDoc = new DocConstructor[docType]
      doc.table_unit.push(newDoc.table_unit[0])

    },
     
    isValid: function () {
      var vm = this
      var result = true
      for (var uid in vm.widgetIsValid) {
        result = result && vm.widgetIsValid[uid]
      }
      return result
    },

  },

  mounted: function () {

  },

  computed: {
  },

  created: function() {
    var vm = this;
    EventBus.$on('widgetState', state => {
      Vue.set(vm.widgetIsValid, state[0], state[1])
    });
  },
  
}
</script>