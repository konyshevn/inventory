<template>
  <div class = "catlg-device-list container">
    <h1 align="left">Устройства</h1>
    <b-container class="text-left">
      <catlg-list-control-panel :status="status"></catlg-list-control-panel>
    </b-container>
    <table class="table table-bordered catlg-list" id="catlg-list">
      <thead>
        <tr>
          <th>У</th>
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
        <tr v-for="device in GETcatlg('device')" :key="device.id">
          <td>
            <b-form-checkbox
            v-model="status.selected"
            :value="device.id"
            >
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
      },
    }
  },
  methods: {
    ...mapActions([
      'FETCHcatlg',
    ]),
    
  },
  computed: {
    ...mapGetters([
      'GETcatlg',
      'GETcatlgItemLabel',
    ]),
  },
  mounted: function () {
    this.FETCHcatlg(['device']);
  },

  created: function () {
  },

  
}
</script>

<style>
.catlg-list td:nth-child(1), .catlg-list th:nth-child(1) {
  width: 50px;
}
.catlg-list td:nth-child(2), .catlg-list th:nth-child(2) {
  width: 150px;
}
.catlg-list td:nth-child(3), .catlg-list th:nth-child(3) {
  width: 250px;
}
.catlg-list td:nth-child(4), .catlg-list th:nth-child(4) {
  width: 250px;
}
.catlg-list td:nth-child(5), .catlg-list th:nth-child(5) {
  width: 250px;
}
.catlg-list td:nth-child(6), .catlg-list th:nth-child(6) {
  width: 150px;
}

</style>