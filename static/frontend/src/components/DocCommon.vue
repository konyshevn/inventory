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
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';

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
        },
        selected: []
      }
    }
  },

  computed: {
    ...mapGetters([
      'currentDoc',
      'currentDocStatus',
      'widgetsIsValid',
    ])
  },

  methods: {
    ...mapActions([
      'PUTcurrentDoc',
      'DELcurrentDoc',
      'DELdoc',
    ]),
    ...mapMutations([
      'UPDcurrentDoc',
    ]),

    fetchDocs (docType) {
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
      errorMsg = errorMsg + JSON.stringify(error)
      if (error.response) {
        if (error.response.data) {
          errorMsg = errorMsg + error.response.data
        }
      } else if (error.message) {
        errorMsg = errorMsg + error.message
      } else if (error.data) {
        errorMsg = errorMsg + error.data
      } else {
        errorMsg = errorMsg + JSON.stringify(error)
      }
      return errorMsg
    },

    sortTU_old: function(TU, field, fieldType){
      var vm = this
      if (vm.tableUnit.sort.field != field) {
        vm.tableUnit.sort.order = -1
      }
      vm.tableUnit.sort.order *= -1
      vm.tableUnit.sort.field = field
      var order = vm.tableUnit.sort.order

      function compareTUrowWidget(a, b) {
        if (!a[field]) return 1;
        if (!b[field]) return -1;

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

    async regWriteDocItem () {
      var vm = this;
      var itemStatus = vm.currentDoc.active
      var isNewDoc = vm.currentDoc.id

      await vm.UPDcurrentDoc(['active', true])
      try {
        if (!vm.widgetsIsValid) { 
          throw new Error('Заполните все необходимые реквизиты документа.')
        }
        var response = await vm.PUTcurrentDoc()
        if (!(isNewDoc) && (response.status == 200 || response.status == 201)) {
          vm.$router.push({ name: 'doc.item', params: {docType: vm.currentDocStatus.docType, id: response.data.id} })
        }
        //vm.$bvModal.show('status-msg')
      } catch(error) {
        await vm.UPDcurrentDoc(['active', itemStatus])
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка проведения: ${vm.getErrorMsg(error)}`])
      }
    },

    async regDelDocItem (docType, item) {
      var vm = this;
      var itemStatus = vm.currentDoc.active
      vm.UPDcurrentDoc(['active', false])
      try {
        if (!vm.widgetsIsValid) { 
          throw new Error('Заполните все необходимые реквизиты документа.')
        }
        var response = await vm.PUTcurrentDoc()
      } catch(error) {
        vm.UPDcurrentDoc(['active', itemStatus])
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка отмены проведения: ${vm.getErrorMsg(error)}`])
      }
    },

    async saveDocItem (docType, item) {
      var vm = this;
      var isNewDoc = vm.currentDoc.id
      try {
        if (!vm.widgetsIsValid) { 
          throw new Error('Заполните все необходимые реквизиты документа.')
        }
        var response = await vm.PUTcurrentDoc()
        if (!(isNewDoc) && (response.status == 200 || response.status == 201)) {
          vm.$router.push({ name: 'doc.item', params: {docType: vm.currentDocStatus.docType, id: response.data.id} })
        }
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
          var response = await vm.DELcurrentDoc()
        } else {
          status = false
        }
      } catch(error) {
        status = false
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка удаления: ${vm.getErrorMsg(error)}`])
      } finally {
        if (status) {
          vm.$router.push({ name: 'doc.list', params: {docType: vm.currentDocStatus.docType} })
        }
      }
    },

  async delDocs (docType, ids) {
      var vm = this;
      try {
        var confirm = await vm.confirmMsg('Вы действительно хотите удалить выделенные документы?')
        if (confirm) {
          ids.forEach(function(item, i, arr){
            vm.DELdoc([docType, item])
          })
        } else {
          status = false
        }
      } catch(error) {
        status = false
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка удаления: ${vm.getErrorMsg(error)}`])
      } 
    },


    addRowTableUnit: function(docType, doc) {
      var vm = this
      var newDoc = new DocConstructor[docType]
      doc.table_unit.push(newDoc.table_unit[0])

    },

    deleteRowTableUnit: function(doc, rowToDelete) {
      var vm = this
      var newRows  = doc.table_unit.filter(function(value){
        return (rowToDelete.indexOf(value.id) >= 0) ? false : true 
      })
      doc.table_unit = newRows

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



  created: function() {
    var vm = this;
    EventBus.$on('widgetState', state => {
      Vue.set(vm.widgetIsValid, state[0], state[1])
    });
  },
  
}
</script>