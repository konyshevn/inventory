<template>
  <div class = "catlg-department-list container">
    <h2 align="left">Подразделения</h2>
    <b-container class="text-left">
      <catlg-list-control-panel :status="status"></catlg-list-control-panel>
    </b-container>
    <table class="table table-bordered catlg-list" id="catlg-list">
      <thead>
        <tr>
          <th><font-awesome-icon icon="check-square"/></th>
          <sort-header :obj-type="{catlg: status.catlgType}" field-type="text" sort-field="label">
            Наименование
          </sort-header>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in GETcatlg(status.catlgType)" :key="item.id" @dblclick="clickRow(item.id, $event)">
          <td>
            <b-form-checkbox
            v-model="status.selected"
            :value="item.id"
            @input="selectedInput">
            </b-form-checkbox>
          </td>
          <td>
            {{item.label}}
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
  name: 'CatlgDepartmentList',
  
  components: {
    SortHeader,
    CatlgListControlPanel,
  },

  mixins: [CatlgCommon],
  
  data () {
    return {
      status: {
        selected: [],
        catlgType: 'department',
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
        this.$router.push({ name: 'catlg.item', params: {id: id, catlgType: vm.status.catlgType} })
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
    if (vm.modal) {vm.status.selected = null}
    this.FETCHcatlg([vm.status.catlgType]);
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
  width: 95%;
}


.catlg-list {
  max-width: 650px;
  min-width: 200px;

}

.catlg-list tbody{
  display:block;
  overflow:auto;
  height: calc(100vh  - 220px);
}
.catlg-list thead tr {
  display: table;
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