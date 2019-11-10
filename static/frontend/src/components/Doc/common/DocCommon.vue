<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import {EventBus} from '@/components/common/event-bus.js'
import Common from '@/components/common/Common.vue';
import * as DocConstructor from '@/components/Doc/common/doc-constructor.js'

export default {
  name: 'DocCommon',
  mixins: [Common],
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


    async regWriteDocItem (parent) {
      var vm = this;
      var itemStatus = vm.currentDoc.active
      var isNewDoc = vm.currentDoc.id
      let response = {}
      let errors = []

      await vm.UPDcurrentDoc(['active', true])
      if (!vm.widgetsIsValid(parent)) {
        response.status = 400
        response.data = `Заполните все необходимые реквизиты.`
      } else {
        response = await vm.PUTcurrentDoc()
      }

      if (response.status == 200 || response.status == 201) {
        if (!(isNewDoc)) {
          vm.$router.push({ name: 'doc.item', params: {docType: vm.currentDocStatus.docType, id: response.data.id} })
        } 
      } else {
        await vm.UPDcurrentDoc(['active', itemStatus])
        errors.push(`Ошибка проведения: ${JSON.stringify(response.data)}`)
        EventBus.$emit('openStatusMsg', errors)
      }

    },

    async regDelDocItem (parent) {
      var vm = this;
      var itemStatus = vm.currentDoc.active
      var response = {}
      var errors = []
      await vm.UPDcurrentDoc(['active', false])
      
      if (!vm.widgetsIsValid(parent)) {
        response.status = 400
        response.data = `Заполните все необходимые реквизиты.`
      } else {
        response = await vm.PUTcurrentDoc()
      }

      if (!(response.status == 200 || response.status == 201)) {
        await vm.UPDcurrentDoc(['active', itemStatus])
        errors.push(`Ошибка отмены проведения: ${JSON.stringify(response.data)}`)
        EventBus.$emit('openStatusMsg', errors)
      }
    },

    async saveDocItem (parent) {
      var vm = this;
      var isNewDoc = vm.currentDoc.id
      var response = {}
      var errors = []

      if (!vm.widgetsIsValid(parent)) {
        response.status = 400
        response.data = `Заполните все необходимые реквизиты.`
      } else {
        response = await vm.PUTcurrentDoc()
      }

      if (response.status == 200 || response.status == 201) {
        if (!(isNewDoc)) {
          vm.$router.push({ name: 'doc.item', params: {docType: vm.currentDocStatus.docType, id: response.data.id} })
        } 
      } else {
        errors.push(`Ошибка проведения: ${JSON.stringify(response.data)}`)
        EventBus.$emit('openStatusMsg', errors)
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