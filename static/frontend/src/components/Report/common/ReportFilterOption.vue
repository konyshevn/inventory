<template>
  
  <b-row align-v="end" class="mb-2">
    <b-col sm="2"><label>{{filterOption.label}}:</label></b-col>
    <b-col sm="7">
      <catlg-widget v-if="isCatlgMulti" 
      :widgetType="filterOption.type.catlg"
      :multi="true"
      :model-multi.sync="filterValueLocal"
      :required="isRequired">
      </catlg-widget>

      <catlg-widget v-if="isCatlgSingle" 
      :widgetType="filterOption.type.catlg"
      :model.sync="filterValueLocal"
      :required="isRequired">
      </catlg-widget>

      <datetime-widget v-if="isDate"
      :date-only="true"
      :model.sync="filterValueLocal">
      </datetime-widget>
    </b-col>
    <b-col sm="1">
      <b-button v-if="isCatlg"
      :disabled="!catlgWidgetMultiSwitch" 
      :pressed.sync="catlgWidgetMulti" 
      variant="light" 
      size="sm">
        Список
      </b-button>
    </b-col>
  </b-row>

</template>


<script>
/* eslint-disable no-console */
// import RepCurrentLocation from '@/components/Report/RepCurrentLocation.vue';



export default {
  name: 'ReportFilterOption',
  components: {
    CatlgWidget: () => import('@/components/Catlg/common/Widget/CatlgWidget.vue'),
    DatetimeWidget: () => import('@/components/Catlg/common/Widget/DatetimeWidget.vue'),

  },

  props: {
    filterOption: Object,
    filterOptionName: String,
    // status: Object,
    filterValue: null,
    parent: null,
  },
  
 
  data () {
    return {
      filterValueLocal: this.filterValue,
      catlgWidgetMulti: false,
    }       
  },

  methods: {

  },

  computed: {
    isCatlg: function(){
      const vm = this
      if (typeof vm.filterOption['type'] === 'object' && 'catlg' in vm.filterOption['type']) {
        return true
      } else {
        return false
      }
    },

    catlgWidgetMultiSwitch: function() {
      const vm = this
      if ('list' in vm.filterOption && vm.filterOption['list']) {
        return true
      } else {
        return false
      }
    },


    isCatlgSingle: function(){
      const vm = this
      if (vm.isCatlg && !vm.catlgWidgetMulti) {
        return true
      } else {
        return false
      }
    },

    isCatlgMulti: function(){
      const vm = this
      if (vm.isCatlg && 'list' in vm.filterOption && vm.filterOption['list'] && vm.catlgWidgetMulti) {
        return true
      } else {
        return false
      }
    },

    isDate: function(){
      const vm = this
      if (vm.filterOption['type'] == 'date') {
        return true
      } else {
        return false
      }
    },

    isDatetime: function(){
      const vm = this
      if (vm.filterOption['type'] == 'datetime') {
        return true
      } else {
        return false
      }
    },

    isRequired: function(){
      const vm = this
      let uid = null
      if (vm.filterOption['required']) {
        uid = vm.parent
      }
      return uid
    },
  },
  
  mounted: function () {
  },

  created: function() {
  }, 

  watch: {
    filterValueLocal: {
      handler(){
        const vm = this
        vm.$emit('update:filter-value', vm.filterValueLocal)
      }
    },
  },
}
   



</script>

<style >

</style>

