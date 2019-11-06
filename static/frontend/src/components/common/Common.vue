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
  },
  
  mounted: function () {
  },

  created: function() {
  }, 

}
   



</script>

<style scoped>

</style>

