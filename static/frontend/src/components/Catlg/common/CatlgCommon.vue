<template>
	<div></div>
</template>

<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import Common from '@/components/common/Common.vue';
import {EventBus} from '@/components/common/event-bus.js'
// var _ = require('lodash');

async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

export default {
	name: 'CatlgCommon',
	mixins: [Common,],
	props: {
		//msg: String
	},
	data () {
		return {
		}
	},

  computed: {
    ...mapGetters([
      'GETcatlgItem',
      'GETcatlgItemLabel',
      'widgetsIsValid',
    ])
  },


	methods: {
  ...mapActions([
    'DELcatlg',
    'PUTcatlg',
	]),
	
		async delCatlgs (status, ids, modal=false) {
      var vm = this;
      var errors = []
      if (!Array.isArray(ids)){
        ids = [ids]
      }
      // console.log('Status', status)
      var confirm = await vm.confirmMsg('Вы действительно хотите удалить выбранные элементы?')
			if (confirm) {
        // console.log('delCatlgs: confirm')
        await asyncForEach(ids, async function(item){
          let response = await vm.DELcatlg([status.catlgType, item])
          // console.log('delCatlgs: response', response)
          if (!(response.status == 200 || response.status == 201 || response.status == 204)) {
            // console.log('delCatlgs', response)
            errors.push(`Ошибка удаления "${vm.GETcatlgItemLabel(status.catlgType, item)}": ${response.data}`)
          }
        })
      
        if (errors.length == 0){
          if (!modal) {
            vm.$router.push({ name: 'catlg.list', params: {catlgType: status.catlgType} })
          } else {
            // console.log('closeCatlgItemModal',  `catlg-item-modal-${status.catlgType}`)
            EventBus.$emit('closeCatlgItemModal', `catlg-item-modal-${status.catlgType}`)
          }
        } else {
          EventBus.$emit('openStatusMsg', errors)
        }
			}
    },
	

		async saveCatlgItem (item, status, parent){
			var vm = this
      var isNewCatlg = item.id ? false : true
      var errors = []
      var response = {}
      let itemSaved = false

      EventBus.$emit('start-saving-catlg', {itemType: status.catlgType, itemId: item.id})
      if (!vm.widgetsIsValid(parent)) {
        response.status = 400
        response.data = `Заполните все необходимые реквизиты.`
      } else {
        response = await vm.PUTcatlg([status.catlgType, item])
      }

      if (response.status == 200 || response.status == 201) {
        itemSaved = true
        if (isNewCatlg) {
          item.id = response.data.id
        }
        if (!status.modalLocal && isNewCatlg) {
          vm.$router.push({ name: 'catlg.item', params: {catlgType: status.catlgType, id: item.id} })
        } 
      } else {
        errors.push(`Ошибка сохранения "${vm.GETcatlgItemLabel(status.catlgType, item.id)}": ${response.data}`)
        EventBus.$emit('openStatusMsg', errors)
      }
      EventBus.$emit('stop-saving-catlg', {itemType: status.catlgType, itemId: item.id, saved: itemSaved})

		},

    editCatlgItemModal: function (catlgType, itemId, modalId=null) {
      if (Array.isArray(itemId)) {
        itemId = itemId[0]
      }
      if (!((itemId == null) || (itemId == undefined))){
        EventBus.$emit('editCatlgItemModal', {catlgType: catlgType, id: itemId, modalId: modalId})
      }
    },

    CatlgClickRow: function (id) {
      const vm = this
      if (vm.modal) {
        EventBus.$emit('modalItemSelected', {modalId: vm.modal, id: id, handleOk: true})
      } else {
        this.$router.push({ name: 'catlg.item', params: {id: id, catlgType: vm.status.catlgType} })
      }
    },

    CatlgSelectedInput: function (event) {
      const vm = this
      if (vm.modal) {
        // console.log('CatlgSelectedInput: event', event)
        EventBus.$emit('modalItemSelected', {modalId: vm.modal, id: Number(event.target.value), handleOk: false})
      }
    },

	},
	
	mounted: function () {


	}
	
}
</script>