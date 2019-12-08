<template>
  <div class="doc-income-item container">
    <div class="container">
    <header>
      <h2>{{docTitle(status.docType)}}</h2>
      <b-badge v-if="false" variant="info">редактируется</b-badge> 
    </header>
      <b-container class="text-left" >
        <doc-item-control-panel :status.sync="status" :item.sync="item"></doc-item-control-panel>
        <p></p>

        <b-row align-v="end" class="mb-2">
          <b-col sm="1"> 
            <label>Номер:</label> 
          </b-col>
          <b-col sm="2">
            <b-form-input v-model="item.doc_num" type="number" number></b-form-input>
          </b-col>
          <b-col sm="1">
            <label>Дата:</label> 
          </b-col>
          <b-col sm="3">
            <datetime-widget v-if="item.doc_date" :model.sync="item.doc_date"></datetime-widget>
          </b-col>
          <b-col sm="2" align="center">
            <b-button v-if="item.active" disabled variant="success">Проведен</b-button>
            <b-button v-if="!item.active" disabled variant="light">Не проведен</b-button>
          </b-col>
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Подразделение:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="department" :required="uid" :model.sync="item.department"></catlg-widget>
            
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Склад:</label>
          </b-col> 
          <b-col sm="5">
            <catlg-widget widget-type="stock" :model.sync="item.stock"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Комментарий:</label>
          </b-col>
          <b-col sm="8" align-h="start"> 
            <b-form-input v-model="item.comment" type="text" maxlength="70"></b-form-input>
          </b-col>
        </b-row>
      </b-container>
      <b-container class="text-left" >
        <table-unit-control-panel :item.sync="item" :status.sync="status"></table-unit-control-panel>
      </b-container>
    </div>

    <div>
      <smart-table 
      :table-padd="400"
      :selected-plural="true"
      :selectAll="true"
      :selectRowClick="false"
      :selected.sync="status.tableUnit.selected"
      :sort-by.sync="status.tableUnit.sortBy"
      :sort-asc.sync="status.tableUnit.sortAsc"
      :items="item.table_unit"
      :fields="[
        {key: 'device', label: 'Устройство', type: 'widget', width: '35%',
        widgetSettings: {required: uid, type: 'device'}
        },
        {key: 'person', label: 'Сотрудник', type: 'widget', width: '25%',
        widgetSettings: {type: 'person'}
        },
        {key: 'qty', label: 'Количество', type: 'input-number', width: '15%',},
        {key: 'comment', label: ' Комментарий', type: 'input-text', width: '20%',},
      ]"
    >
      
    </smart-table>

  </div>

  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';
import DatetimeWidget from '@/components/Catlg/common/Widget/DatetimeWidget.vue';
import DocItemControlPanel from '@/components/Doc/common/ControlPanel/DocItemControlPanel.vue';
import TableUnitControlPanel from '@/components/Doc/common/ControlPanel/TableUnitControlPanel.vue';
import SmartTable from '@/components/common/SmartTable.vue'
import * as DocConstructor from '@/components/Doc/common/doc-constructor.js'


function mapTwoWay (key, getter, mutation) {
  return {
    get () {
      return this.$store.getters[getter][key]
    },
    set (value) {
      this.$store.commit(mutation, [key, value])
    }
  }
}

export default {
  name: 'DocIncomeItem',
  components: {
    CatlgWidget,
    DatetimeWidget,
    DocItemControlPanel,
    TableUnitControlPanel,
    SmartTable,
  },

  mixins: [CatlgCommon, DocCommon],
  
  props: {
    id: String,
  },
    
  data () {
    return {
      status: {
        docType: 'docincome',
        docChanged: false,
        uid: null,
        tableUnit: {
          sortBy: "", 
          sortAsc: true,
          selected: [],
        },
      },
      item: {},
    }       
  },

  methods: {
    ...mapMutations([
    ]),

    ...mapActions([
      'FETCHdocItem',
    ])
  },

  computed: {
    ...mapGetters([
      'widgetsIsValid',
      'GETdocItem',

    ])
  },

 
  async mounted () {
    const vm = this
    vm.status.uid = vm.uid
    if (vm.id == "new") {
      vm.item = new DocConstructor[vm.status.docType]
      //vm.DELcurrentDoc()
      //vm.INITcurrentDoc(vm.docType)
    } else {
      await vm.FETCHdocItem([vm.status.docType, vm.id])
      vm.item = vm.GETdocItem(vm.status.docType, vm.id)
    }
  },

  created: function() {
  }, 

  beforeDestroy: function() {
    //this.DELcurrentDoc()
  },

}
   



</script>

<style >


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

