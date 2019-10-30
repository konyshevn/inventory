<template>
  <div class="catlg-device-item container" >
    <div class="container">
    <header>
      <h2 align="left">Устройство</h2>
      <b-badge v-if="false" variant="info">редактируется</b-badge> 
    </header>
    </div>
    <catlg-item-control-panel :item="item" :catlgType="catlgType"></catlg-item-control-panel>
    <div>
      <b-table-simple small class="table-borderless" style="width: 500px">
        <b-tr>
          <b-td>
            Тип
          </b-td>
          <b-td >
            <catlg-widget widget-type="deviceType" :model.sync="item.deviceType" required></catlg-widget>
          </b-td>
        </b-tr>

        <b-tr>
          <b-td>
            Наименование
          </b-td>
          <b-td>
            <catlg-widget widget-type="nomenclature" :model.sync="item.nomenclature" required></catlg-widget>
          </b-td>
        </b-tr>
        
        <b-tr>
          <b-td>
            Серийный номер
          </b-td>
          <b-td>
            <b-form-input v-model="item.serial_num" type="text"></b-form-input>
          </b-td>
        </b-tr>
        
        <b-tr>
          <b-td>
            Инвентарный номер
          </b-td>
          <b-td>
            <b-form-input v-model="item.inv_num" type="text"></b-form-input>
          </b-td>
        </b-tr>
        
        <b-tr>
          <b-td>
            Комментарий
          </b-td>
          <b-td>
            <b-form-input v-model="item.comment" type="text"></b-form-input>
          </b-td>
        </b-tr>
      </b-table-simple>
    </div>

  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import CatlgItemControlPanel from '@/components/Catlg/common/ControlPanel/CatlgItemControlPanel.vue';
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget2.vue';
import CatlgWidgetModal from '@/components/Catlg/common/Widget/CatlgWidgetModal.vue';
import SortHeader from '@/components/common/SortHeader.vue'
import * as CatlgConstructor from '@/components/Catlg/common/catlg-constructor.js'



export default {
  name: 'CatlgDeviceItem',
  components: {
    CatlgWidget,
    CatlgWidgetModal,
    SortHeader,
    CatlgItemControlPanel,

  },
  props: {
    id: Number,
  },
  
  mixins: [CatlgCommon,],
  
  data () {
    return {
      catlgType: 'device',
      item: {},
    }       
  },

  methods: {
    ...mapMutations([
    ]),

    ...mapActions([
      'FETCHcatlgItem',
    ])
  },

  computed: {
    ...mapGetters([
      'GETcatlgItem',

    ])
  },

 /*
  mounted: function () {
    var vm = this
    //this.$nextTick(function () {
    //  vm.getDocItem('docincome', vm.id);
    //})
    if (vm.id == "new") {
      vm.DELcurrentDoc()
      vm.INITcurrentDoc('docincome')
    } else {
      vm.FETCHcatlgItem(['device', vm.id])
      vm.item = vm.GETcatlgItem('device', vm.id)
    }
  },
*/
   async mounted () {
    var vm = this
    if (vm.id == 'new') {
      vm.item = new CatlgConstructor['device']
      //Vue.set(vm, 'item', new CatlgConstructor['device'])
    } else {
      await vm.FETCHcatlgItem(['device', vm.id])
      vm.item = vm.GETcatlgItem('device', vm.id)
    }
  },

  created: function() {
  }, 

  beforeDestroy: function() {
    console.log('beforeDestroy')
  },

}
   



</script>

<style >
.table_unit tbody tr:hover {
    background-color: #f2f2f2;
    color: #000000
  }

.table_unit td, .table_unit th {
  padding: 0.30rem !important;
}


.table_unit td:nth-child(1), .table_unit th:nth-child(1) {
  width: 5%;
}
.table_unit td:nth-child(2), .table_unit th:nth-child(2) {
  width: 35%;
}
.table_unit td:nth-child(3), .table_unit th:nth-child(3) {
  width: 25%;
}
.table_unit td:nth-child(4), .table_unit th:nth-child(4) {
  width: 15%;
}
.table_unit td:nth-child(5), .table_unit th:nth-child(5) {
  width: 20%;
}

.table_unit {
  display: inline-grid;
  grid-template-areas: 
  "head-fixed" 
  "body-scrollable";
}

.table_unit thead {
  grid-area: head-fixed;
  /* fallback */
  width: 100%;
  /* minus scroll bar width */
  width: calc( 100% - 1em ) !important;/* scrollbar is average 1em/16px width, remove it from thead width */
  cursor: pointer;
}

.table_unit tbody {
  grid-area: body-scrollable;
  overflow-y: scroll;
  height: calc(90vh  - 350px);
}


.table_unit thead, .table_unit tbody tr {
    display:table;
    table-layout:fixed;/* even columns width , fix width of table too*/
}

.select-row {
  vertical-align: middle; 
  text-align: center;
}

header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}


</style>

