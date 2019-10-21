<template>
  <div class = "catlg-device-list container">
    <h1 align="left">Устройства</h1>
    <b-container class="text-left">
      <catlg-list-control-panel :status="status"></catlg-list-control-panel>
    </b-container>

    <b-table
      striped 
      hover
      small
      bordered
      sort-null-last
      primary-key="id"
      :sort-compare="compareTUrowWidget"
      :filter="status.tableFilter"
      sticky-header="calc(100vh  - 180px)"
      :items="items"
      :fields="[
        {key: 'deviceType', label: 'Тип', sortable: true, sortByFormatted: false, filterByFormatted: true,
          formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'nomenclature', label: 'Наименование', sortable: true, sortByFormatted: true, filterByFormatted: true,
          formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'serial_num', label: 'Серийный номер', sortable: true},
        {key: 'inv_num', label: 'Инвентарный номер', sortable: true},
        {key: 'comment', label: ' Комментарий', sortable: true},
      ]"
    >
    </b-table>


  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import SortHeader from '@/components/common/SortHeader.vue'
import CatlgListControlPanel from '@/components/Catlg/common/ControlPanel/CatlgListControlPanel.vue'
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';


export default {
  name: 'CatlgDeviceList',
  
  components: {
    SortHeader,
    CatlgListControlPanel,
  },

  mixins: [CatlgCommon],
  
  data () {
    return {
      items: [],
      status: {
        selected: [],
        tableFilter: null,
      },
    }
  },
  methods: {
    ...mapActions([
      'FETCHcatlg',
    ]),

    compareTUrowWidget: function (a, b, field) {
        var vm = this
        if (!a[field]) return 1;
        if (!b[field]) return -1;

        
        //let catlgItemA = _.find(state.catlgs[field]['data'], {id: a[field]})
        //let catlgItemB = _.find(state.catlgs[field]['data'], {id: b[field]})
        var aLabel = vm.GETcatlgItemLabel(field, a[field])
        var bLabel = vm.GETcatlgItemLabel(field, b[field])
        return aLabel < bLabel ? 1 : -1;
      },
    
  },
  computed: {
    ...mapGetters([
      'GETcatlg',
      'GETcatlgItemLabel',
    ]),
  },
  mounted: function () {
    this.FETCHcatlg(['device']);
    this.items = this.GETcatlg('device')
  },

  created: function () {
  },

  
}
</script>

<style>
.catlg-list td:nth-child(1), .catlg-list th:nth-child(1) {
  width: 5%;
}
.catlg-list td:nth-child(2), .catlg-list th:nth-child(2) {
  width: 20%;
}
.catlg-list td:nth-child(3), .catlg-list th:nth-child(3) {
  width: 20%;
}
.catlg-list td:nth-child(4), .catlg-list th:nth-child(4) {
  width: 25%;
}
.catlg-list td:nth-child(5), .catlg-list th:nth-child(5) {
  width: 15%;
}
.catlg-list td:nth-child(6), .catlg-list th:nth-child(6) {
  width: 15%;
}

.catlg-list tbody{
  display:block;
  overflow:auto;
  min-width: 1000px;
  height: calc(100vh  - 250px);
}
.catlg-list thead tr{
  display:table;
  width: calc( 100% - 1em ) !important;
}

.catlg-list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}




</style>