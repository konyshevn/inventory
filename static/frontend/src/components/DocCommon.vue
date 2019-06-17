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

    async regWriteDocItem (docType, item) {
      var vm = this;
      item.active = true
      try {

        if (!vm.isValid()) { 
          throw new Error('Заполните все необходимые реквизиты документа.')
        }
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
        
        //vm.$bvModal.show('status-msg')
      } catch(error) {
        item.active = false
        console.log(error)
        var errorMsg = ''
        if (error.response) {
          errorMsg = (error.response.data) ? error.response.data : errorMsg
        } else if (error.message) {
          errorMsg = errorMsg + error.message
        }
        EventBus.$emit('openStatusMsg', [`Ошибка проведения: ${errorMsg}`])
      }
    },

    async regDelDocItem (docType, item) {
      var vm = this;
      var itemStatus = item.active
      item.active = false
      try {
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
      } catch(error) {
        item.active = itemStatus
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка отмены проведения: ${error.response.data}`])
      }
    },

    async saveDocItem (docType, item) {
      var vm = this;
      try {
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
      } catch(error) {
        console.log(error)
        console.log(error.response.data)
        EventBus.$emit('openStatusMsg', [`Ошибка сохранения: ${error.response.data}`])
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
        EventBus.$emit('openStatusMsg', [`Ошибка удаления: ${error.response.data}`])
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