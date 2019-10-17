<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import Common from '@/components/common/Common.vue';
import * as DocConstructor from '@/components/Doc/common/doc-constructor.js'

export default {
  name: 'DocCommon',
  mixins: [Common, CatlgCommon],
  props: {
    //msg: String
  },
  data () {
    return {
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
    
 },

  mounted: function () {
  },

  created: function() {
  },
  
}
</script>