<template>
  <div class="container">
  <b-overlay
  id="overlay-background"
  :show="status.itemSaving"
  variant="white"
  opacity="0.40"
  blur="2px"
  rounded="sm"
  >
    <vue-headful :title="docItemTitle(status.docType, item.id)"/>
    <div class="container">
    <header>
      <h2>{{docTitle(status.docType)}}</h2>
      <item-changed :item="item" :status="status"></item-changed>
    </header>
      <b-container class="text-left" >
        <doc-item-control-panel :status.sync="status" :item.sync="item">
          <b-dropdown text="Создать на основании" right variant="light" size="sm">
            <b-dropdown-item @click="createDocFollower(status.docType, item.id, 'docincome')" :disabled="!item.id">
              Оприходование
            </b-dropdown-item>
            <b-dropdown-item @click="createDocFollower(status.docType, item.id, 'docwriteoff')" :disabled="!item.id">
              Списание
            </b-dropdown-item>
            <b-dropdown-item @click="createDocFollower(status.docType, item.id, 'docmove')" :disabled="!item.id">
              Перемещение
            </b-dropdown-item>
          </b-dropdown>
        </doc-item-control-panel>

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
          <b-col sm="2">
            <datetime-widget :model.sync="item.doc_date"></datetime-widget>
          </b-col>
          <b-col sm="2" align="center">
            <b-button v-if="item.active" :to="{path: 'registry-list'}" append target="_blank" variant="success">Проведен</b-button>
            <b-button v-if="!item.active" disabled variant="light">Не проведен</b-button>
          </b-col>
          <b-col sm="1" align="center">
            <b-button v-b-modal.doc-follower variant="info">Иерархия</b-button>
          </b-col>
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start" >
            <label>Подразделение:</label>
          </b-col> 
          <b-col sm="4">
            <catlg-widget widget-type="department" :required="uid" :model.sync="item.department"></catlg-widget>
          </b-col> 
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Склад:</label>
          </b-col> 
          <b-col sm="4">
            <catlg-widget widget-type="stock" :model.sync="item.stock"></catlg-widget>
          </b-col>
        </b-row>

        <b-row align-v="end" class="mb-2">
          <b-col sm="2" align-h="start">
            <label>Комментарий:</label>
          </b-col>
          <b-col sm="6" align-h="start"> 
            <b-form-input v-model="item.comment" type="text" maxlength="70"></b-form-input>
          </b-col>
        </b-row>
      </b-container>
      <b-container class="text-left" >
        <table-unit-control-panel :item.sync="item" :status.sync="status">
          <b-button variant="light" size="sm" @click="fillSaldo">Заполнить остатками</b-button>
        </table-unit-control-panel>
      </b-container>
    </div>

    <div>
      <smart-table 
      :table-padd="200"
      :selected-plural="true"
      :select-all="true"
      :select-row-click="false"
      :selected.sync="status.tableUnit.selected"
      :sort-by.sync="status.tableUnit.sortBy"
      :sort-asc.sync="status.tableUnit.sortAsc"
      :items="item.table_unit"
      :fields="[
        {key: 'device', label: 'Устройство', type: 'widget', width: '20%',
        widgetSettings: {required: uid, type: 'device'}
        },
        {key: 'person_accountg', label: 'Сотрудник (учет)', type: 'widget', width: '15%',
        widgetSettings: {type: 'person'}
        },
        {key: 'qty_accountg', label: 'Количество (учет)', type: 'input-number', width: '10%',},
        {key: 'person_fact', label: 'Сотрудник (факт)', type: 'widget', width: '15%',
        widgetSettings: {type: 'person'}
        },
        {key: 'qty_fact', label: 'Количество (факт)', type: 'input-number', width: '10%',},
        {key: 'stock_fact', label: 'Склад (факт)', type: 'widget', width: '15%',
        widgetSettings: {type: 'stock'}
        },
        {key: 'comment', label: ' Комментарий', type: 'input-text', width: '10%',},
      ]"
      >
      </smart-table>

  </div>
  </b-overlay>
  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapActions } from 'vuex';
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';
import DatetimeWidget from '@/components/Catlg/common/Widget/DatetimeWidget.vue';
import DocItemControlPanel from '@/components/Doc/common/ControlPanel/DocItemControlPanel.vue';
import TableUnitControlPanel from '@/components/Doc/common/ControlPanel/TableUnitControlPanel.vue';
import SmartTable from '@/components/common/SmartTable.vue'
import ItemChanged from '@/components/common/ItemChanged.vue';
import DocItemMixin from '@/components/Doc/common/DocItemMixin.vue';

export default {
  name: 'DocInventoryItem',
  components: {
    CatlgWidget,
    DatetimeWidget,
    DocItemControlPanel,
    TableUnitControlPanel,
    SmartTable,
    ItemChanged,
  },

  mixins: [DocItemMixin, DocCommon],
  
  props: {
    id: String,
  },
    
  data () {
    return {
      status: {
        docType: 'docinventory',
        uid: null,
        tableUnit: {
          sortBy: "", 
          sortAsc: true,
          selected: [],
        },
        itemSaving: false,
      },
      item: {},
    }       
  },

  methods: {
    ...mapActions([
      'FETCHdocItemExtra',
    ]),

    async fillSaldo () {
      const vm = this
      var confirm = await vm.confirmMsg('Документ будет сохранен. Продолжить?')
      if (confirm) {
        vm.$on('update:item', item => {
          vm.item = item
        })
        await vm.saveDocItem(vm.status, vm.item)
        let tableUnitFilledSaldo = await vm.FETCHdocItemExtra([vm.status.docType, vm.item.id, 'fill_saldo'])
        vm.item.table_unit.forEach(function(item){
          item.DELETE = true
        })
        vm.item.table_unit = [...vm.item.table_unit, ...tableUnitFilledSaldo];
      }      
    },
  },

  computed: {
  },

}
   



</script>

<style scoped="">
.container {
  max-width: 1300px !important;
}

</style>

