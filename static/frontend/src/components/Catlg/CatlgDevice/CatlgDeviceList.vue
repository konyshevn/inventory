<template>
  <div class = "catlg-device-list container">
    <h1 align="left">Устройства</h1>
    <table class="table table-bordered">
      <thead>
        <tr>
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
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';


export default {
  name: 'CatlgDeviceList',
  
  components: {
    SortHeader,
  },

  mixins: [CatlgCommon],
  
  data () {
    return {
      type: 'CatlgList'
    }
  },
  methods: {
    ...mapActions([
      'FETCHcatlg',
    ]),
    
    async loadCatlgList () {
      var vm = this
      await vm.fetchCatlg('device')
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
  },

  created: function () {
  },

  
}
</script>