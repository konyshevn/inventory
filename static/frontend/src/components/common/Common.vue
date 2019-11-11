<template>
  <div>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import {aliases} from '@/components/common/aliases.js';


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

    docTitle(docType, type='singular'){
      let title = 'unknown'
      if (type == 'singular'){
        title = aliases.docAlias[docType]['titleSingular']
      } else if (type == 'plural') {
        title = aliases.docAlias[docType]['titlePlural']
      }
      return title
    },

    selectRow: function (id, event) {
      const vm = this
      if (event.srcElement.className == 'custom-control-label') { return }
      if (!vm.modal) {
        let idIndex = vm.status.selected.indexOf(id)
        let result = (idIndex >= 0) ? vm.status.selected.splice(idIndex, 1) : vm.status.selected.push(id)
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

  },

  computed: {
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

