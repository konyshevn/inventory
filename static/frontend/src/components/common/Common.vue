<template>
  <div>
  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import {aliases} from '@/components/common/aliases.js';
import moment from 'moment';


export default {
  name: 'Common',
  components: {
  },

  props: {
  },
  
 
  data () {
    return {
    }       
  },

  methods: {
    async confirmMsg (msg='') {
      var vm = this
      var value = await vm.$bvModal.msgBoxConfirm(msg, {
        title: 'Внимание',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'Да',
        cancelTitle: 'Нет',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
      return value
    },

    catlgTitle(catlgType, type='singular'){
      let title = 'unknown'
      if (type == 'singular'){
        title = aliases.catlgAlias[catlgType]['titleSingular']
      } else if (type == 'plural') {
        title = aliases.catlgAlias[catlgType]['titlePlural']
      }
      return title
    },

    catlgItemTitle(catlgType, catlgId){
      const vm = this
      let title
      // console.log(catlgType, catlgId)
      if (catlgId == 'new' || !catlgId) {
        title = vm.catlgTitle(catlgType)
      } else {
        title = vm.GETcatlgItemLabel(catlgType, catlgId)
      }
      return title
    },

    docTitle(docType, type='singular'){
      let title = 'unknown'
      if (type == 'singular'){
        title = aliases.docAlias[docType]['titleSingular']
      } else if (type == 'plural') {
        title = aliases.docAlias[docType]['titlePlural']
      }
      return title
    },

    docItemTitle(docType, docId){
      const vm = this
      // console.log('docItemTitle', docType, docId)
      let title = ''
      if (docType == undefined || docType == null) {
        title = ''
      } else if (docId == 'new' || docId == undefined){
        title = `${vm.docTitle(docType)} №`
      } else {
        let item = vm.GETdocItem(docType, docId)
        title = (item) ? `${vm.docTitle(docType)} № ${item.doc_num} от ${vm.dateFormat(item.doc_date)}` : ''
      }
      return title
    },

    dateFormat(date){
      return moment(String(date)).format('DD.MM.YYYY HH:mm:ss')
    },

    selectRow: function (id, event) {
      const vm = this
      if (event.srcElement.className == 'custom-control-label') { return }
      if (!vm.modal) {
        let idIndex = vm.status.selected.indexOf(id)
        if (idIndex >= 0) {
          vm.status.selected.splice(idIndex, 1)
        } else {
          vm.status.selected.push(id)
        }
        //let result = (idIndex >= 0) ? vm.status.selected.splice(idIndex, 1) : vm.status.selected.push(id)
      } else {
        vm.status.selected = (vm.status.selected == id) ? null : id
      }
    },

    selectAllRows: function (items) {
      const vm = this
      if (vm.modal) {return}
      if (vm.status.selected >= 0) {
        vm.status.selected = []
        items.forEach(function(item){
          vm.status.selected.push(item.id)
        })
      } else {
        vm.status.selected = []
      }
    },

    isRowSelected: function (id) {
      const vm = this
      let result = false
      if (!vm.modal) {
        let idIndex = vm.status.selected.indexOf(id)
        result = (idIndex >= 0) ? true : false
      } else {
        result = (vm.status.selected == id) ? true : false
      }
      return result

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

    formatDate: function(value) {
      return moment(String(value)).format('DD.MM.YYYY HH:mm:ss')
    },

    mapTwoWay: function (key, getter, mutation) {
      return {
        get () {
          return this.$store.getters[getter][key]
        },
        set (value) {
          this.$store.commit(mutation, [key, value])
        }
      }
    },

  },

  computed: {
    ...mapGetters([
      'GETdocItem',
      'GETcatlgItemLabel',
    ]),

    uid: function () {
      return String(this._uid)
    },

  },
  
  mounted: function () {
  },

  created: function() {
  }, 

}
   



</script>

<style scoped>

</style>

