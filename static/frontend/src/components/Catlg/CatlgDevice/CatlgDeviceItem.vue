<template>
  <div class="catlg-device-item container" >
    <vue-headful v-if="!modal" :title="catlgItemTitle(catlgType, item.id)"/>
    <div class="container">
    <header>
      <h2>{{catlgTitle(catlgType)}}</h2>
      <b-badge v-if="false" variant="info">редактируется</b-badge> 
    </header>
    </div>
    <catlg-item-control-panel :item="item" :catlgType="catlgType" :parent="uid" style="padding-top: 20px"></catlg-item-control-panel>
    <div style="padding-top: 20px">
      <b-table-simple small class="table-borderless" style="width: 500px;">
        <tr>
          <td class="align-middle" style="width: 40%">
            Тип
          </td>
          <td >
            <catlg-widget widget-type="deviceType" :model.sync="item.deviceType" :required="uid"></catlg-widget>
          </td>
        </tr>

        <tr>
          <td class="align-middle" style="width: 40%">
            Наименование
          </td>
          <td>
            <catlg-widget widget-type="nomenclature" :model.sync="item.nomenclature" :required="uid"></catlg-widget>
          </td>
        </tr>
        
        <tr>
          <td class="align-middle" style="width: 40%">
            Серийный номер
          </td>
          <td>
            <b-form-input v-model="item.serial_num" type="text"></b-form-input>
          </td>
        </tr>
        
        <tr>
          <td class="align-middle" style="width: 40%">
            Инвентарный номер
          </td>
          <td>
            <b-form-input v-model="item.inv_num" type="text"></b-form-input>
          </td>
        </tr>
        
        <tr>
          <td class="align-middle" style="width: 40%">
            Комментарий
          </td>
          <td>
            <b-form-input v-model="item.comment" type="text"></b-form-input>
          </td>
        </tr>
      </b-table-simple>
    </div>
  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import CatlgItemControlPanel from '@/components/Catlg/common/ControlPanel/CatlgItemControlPanel.vue';
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';
import * as CatlgConstructor from '@/components/Catlg/common/catlg-constructor.js'



export default {
  name: 'CatlgDeviceItem',
  components: {
    CatlgWidget,
    CatlgItemControlPanel,
  },

  props: {
    id: String,
    modal: {
      type: Boolean,
      default: false,
    },
  },
  
  mixins: [CatlgCommon,],
  
  data () {
    return {
      catlgType: 'device',
      item: {},
      widgetIsValid: {},
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
      'widgetsIsValid',
    ]),

  },

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


</style>

