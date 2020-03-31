<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import {EventBus} from '@/components/common/event-bus.js'
import Common from '@/components/common/Common.vue';
var _ = require('lodash');


async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}


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
      'widgetsIsValid',
    ]),

    docChanged: function () {
      const vm = this
      return !_.isEqual(vm.item, vm.itemInit);
    },
  },

  methods: {
    ...mapActions([
      'PUTdoc',
      'PUTcurrentDoc',
      'DELcurrentDoc',
      'DELdoc',
      'CREATEdocFollower',
      'FETCHdocItem',
    ]),
    ...mapMutations([
      'UPDcurrentDoc',
    ]),


    async regWriteDocItem (status, item) {
      var vm = this;
      let response = {}
      let errors = []
      let itemLocal = _.cloneDeep(item)
      itemLocal.active = true
      let itemSaved = false

      EventBus.$emit('start-saving-doc', {itemType: status.docType, itemId: item.id})

      if (!vm.widgetsIsValid(status.uid)) {
        response.status = 400
        response.data = `Заполните все необходимые реквизиты.`
      } else {
        response = await vm.PUTdoc([status.docType, itemLocal])
      }
      if (response.status >= 200 && response.status < 300) {
        itemLocal = response.data
        itemSaved = true
        if (!(item.id)) {
          vm.$router.push({ name: 'doc.item', params: {docType: status.docType, id: itemLocal.id} })
        } 
      } else {
        itemLocal.active = false
        errors.push(`Ошибка проведения: ${JSON.stringify(response.data)}`)
        EventBus.$emit('openStatusMsg', errors)
      }
      await vm.$emit('update:item', itemLocal)
      EventBus.$emit('stop-saving-doc', {itemType: status.docType, itemId: itemLocal.id, saved: itemSaved})


    },

    async regDelDocItem (status, item) {
      var vm = this;
      var response = {}
      var errors = []
      let itemLocal = _.cloneDeep(item)
      itemLocal.active = false
      let itemSaved = false

      EventBus.$emit('start-saving-doc', {itemType: status.docType, itemId: item.id})      
      if (!vm.widgetsIsValid(status.uid)) {
        response.status = 400
        response.data = `Заполните все необходимые реквизиты.`
      } else {
        response = await vm.PUTdoc([status.docType, itemLocal])
      }

      if (response.status >= 200 && response.status < 300) {
        itemLocal = response.data
        itemSaved = true
        if (!(item.id)) {
          vm.$router.push({ name: 'doc.item', params: {docType: status.docType, id: itemLocal.id} })
        }
      } else {
        errors.push(`Ошибка проведения: ${JSON.stringify(response.data)}`)
        EventBus.$emit('openStatusMsg', errors)
      }
      await vm.$emit('update:item', itemLocal)
      EventBus.$emit('stop-saving-doc', {itemType: status.docType, itemId: itemLocal.id, saved: itemSaved})

    },

    async saveDocItem (status, item) {
      var vm = this;
      var response = {}
      var errors = []
      let itemLocal = _.cloneDeep(item)
      let itemSaved = false

      EventBus.$emit('start-saving-doc', {itemType: status.docType, itemId: item.id})
      if (!vm.widgetsIsValid(status.uid)) {
        response.status = 400
        response.data = `Заполните все необходимые реквизиты.`
      } else {
        response = await vm.PUTdoc([status.docType, itemLocal])
      }

      if (response.status >= 200 && response.status < 300) {
        itemLocal = response.data
        itemSaved = true
        if (!(item.id)) {
          vm.$router.push({ name: 'doc.item', params: {docType: status.docType, id: itemLocal.id} })
        }
      } else {
        itemLocal.active = false
        errors.push(`Ошибка проведения: ${JSON.stringify(response.data)}`)
        EventBus.$emit('openStatusMsg', errors)
      }
      await vm.$emit('update:item', itemLocal)
      EventBus.$emit('stop-saving-doc', {itemType: status.docType, itemId: itemLocal.id, saved: itemSaved})

    },

    async delDocItem (status, item) {
      var vm = this;
      var response = {}
      var errors = []

      var confirm = await vm.confirmMsg('Вы действительно хотите удалить документ?')
      if (confirm) {
        response = await vm.DELdoc([status.docType, item.id])
        if (response.status >= 200 && response.status < 300) {
          vm.$router.push({ name: 'doc.list', params: {docType: status.docType} })
        } else {
          errors.push(`Ошибка проведения: ${JSON.stringify(response.data)}`)
          EventBus.$emit('openStatusMsg', errors)
        }
      } 
    },

  async delDocs (docType, ids) {
      var vm = this;
      var response = {}
      var errors = []
      var confirm = await vm.confirmMsg('Вы действительно хотите удалить выделенные документы?')
      if (confirm) {
        await asyncForEach(ids, async function(item){
          response = await vm.DELdoc([docType, item])
          if (!(response.status >= 200 && response.status < 300)) {
            errors.push(`Ошибка удаления: ${JSON.stringify(response.data)}`)
          }
        })
        if (errors.length > 0){
          EventBus.$emit('openStatusMsg', errors)
        }
      }
    },

    async createDocFollower (docType, id, followerType) {
      const vm = this
      let msgs = ['Были созданы следующие документы, откройте их чтобы провести:']
      let followers = await vm.CREATEdocFollower([docType, id, followerType])
      if (followers.length > 0) {
        await asyncForEach(followers, async function(follower){
          await vm.FETCHdocItem([followerType, follower.id])
          msgs.push([{
            type: 'router-link',
            settings: {name: 'doc.item', params: {docType: followerType, id: follower.id}},
            data: vm.docItemTitle(followerType, follower.id),
          }])
        })
        EventBus.$emit('created-doc-follower', {docType: docType, docId: id})
      }

      EventBus.$emit('openStatusMsg', msgs)
    },
    

    DocClickRow: function (id) {
      const vm = this
      this.$router.push({ name: 'doc.item', params: {id: id, docType: vm.status.docType} })
    },


    DocSelectedInput: function (id, event) {
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

    
 },

  mounted: function () {
  },

  created: function() {
  },
  
}
</script>