<template>
  <div>
    <b-button-group align="left">
      <b-button variant="light" size="sm" @click="addTUrow">Добавить строку</b-button>
      <b-button variant="light" size="sm" @click="delTUrow">Удалить строку</b-button>
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import * as DocConstructor from '@/components/Doc/common/doc-constructor.js'
var _ = require('lodash');


export default {
  name: 'TableUnitControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
    item: Object,
    status: Object,
  },

  data () {
    return {
    }
  },
  methods: {
    addTUrow: function() {
      const vm = this
      let newDoc = new DocConstructor[vm.status.docType]
      let itemLocal = _.cloneDeep(vm.item)
      itemLocal.table_unit.push(newDoc.table_unit[0])
      vm.$emit('update:item', itemLocal)
    },

    delTUrow: function() {
      const vm = this
      let rowToDelete = vm.status.tableUnit.selected
      console.log('rowToDelete', rowToDelete)
      let itemLocal = _.cloneDeep(vm.item)
      console.log('itemLocal:before', itemLocal)
      itemLocal.table_unit.forEach(function(item){
        if ((rowToDelete.indexOf(item.id) >= 0) || (rowToDelete.indexOf(String(item.id)) >= 0)) {
          item.DELETE = true
        } 
      })

      console.log('itemLocal:after', itemLocal)
      vm.$emit('update:item', itemLocal)
      let statusLocal = _.cloneDeep(vm.status)
      statusLocal.tableUnit.selected = []
      vm.$emit('update:status', statusLocal)
    },

  },

  mounted: function () {
  },

  created: function () {
  },
  
}
</script>