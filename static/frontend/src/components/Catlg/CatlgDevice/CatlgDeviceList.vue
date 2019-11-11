<template>
  <div class = "catlg-device-list container">
    <h2 v-if="!modal" align="left">{{catlgTitle(status.catlgType, 'plural')}}</h2>
    <b-container class="text-left">
      <catlg-list-control-panel :status="status"></catlg-list-control-panel>
    </b-container>
    <table class="table table-bordered catlg-list" :id="`catlg-list-${status.catlgType}`">
      <thead>
        <tr>
          <th @click="selectAllRows(GETcatlg(status.catlgType))"><font-awesome-icon icon="check-square"/></th>
          <sort-header :obj-type="{catlg: 'device'}" field-type="widget" sort-field="deviceType">
            Тип
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="label">
            Наименование
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="serial_num">
            Серийный номер
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="inv_num">
            Инвентарный номер
          </sort-header>
          <sort-header :obj-type="{catlg: 'device'}" field-type="text" sort-field="comment">
            Комментарий
          </sort-header>

        </tr>
      </thead>
      <tbody>
        <tr v-for="device in GETcatlg(status.catlgType)" :key="device.id" 
        @dblclick="clickRow(device.id, $event)" 
        @click="selectRow(device.id, $event)"
        :class="{'row-selected': isRowSelected(device.id)}">
          <td>
            <b-form-checkbox
            v-model="status.selected"
            :value="device.id"
            @input="selectedInput"
            class="row-checkbox">
            </b-form-checkbox>
          </td>
          <td>
            {{GETcatlgItemLabel('deviceType', device.deviceType)}}
          </td>
          <td>
            {{GETcatlgItemLabel('nomenclature', device.nomenclature)}}
          </td>
          <td>
            {{device.serial_num}}
          </td>
          <td>
            {{device.inv_num}}
          </td>
          <td>
            {{device.comment}}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import SortHeader from '@/components/common/SortHeader.vue'
import CatlgListControlPanel from '@/components/Catlg/common/ControlPanel/CatlgListControlPanel.vue'
import {EventBus} from '@/components/common/event-bus.js'

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
      status: {
        selected: [],
        catlgType: 'device',
        modal: null,
      },
    }
  },

  props: {
    modal: null,
  },

  methods: {
    ...mapActions([
      'FETCHcatlg',
    ]),

    clickRow: function (id, event) {
      const vm = this
      if (vm.modal) {
        EventBus.$emit('modalItemSelected', {modalId: vm.modal, id: id, handleOk: true})
      } else {
        this.$router.push({ name: 'catlg.item', params: {id: id, catlgType: 'device'} })
      }
    },



    selectedInput: function (value) {
      const vm = this
      if (vm.modal) {
        EventBus.$emit('modalItemSelected', {modalId: vm.modal, id: value, handleOk: false})
      }
    },
  },
  computed: {
    ...mapGetters([
      'GETcatlg',
      'GETcatlgItemLabel',
    ]),
  },
  mounted: function () {
    const vm = this
    vm.status.modal = vm.modal
    if (vm.modal) {vm.status.selected = ''}
    this.FETCHcatlg(['device']);
  },

  created: function () {
  },

  
}
</script>

<style scoped>
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
  height: calc(100vh  - 220px);
}

.catlg-list thead tr{
  display:block;
  width: calc( 100% - 1em ) !important;
  cursor: pointer;
}

.catlg-list tbody tr:hover {
background-color: #f2f2f2;
color: #000000
}

.catlg-list th, .catlg-list td {
padding: 0.25rem !important;
}



</style>