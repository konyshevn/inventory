<template>
  <div class="catlg-device-item container" >
  <b-overlay
  id="overlay-background"
  :show="status.itemSaving"
  variant="white"
  opacity="0.40"
  blur="2px"
  rounded="sm"
  >
    <vue-headful v-if="!modal" :title="catlgItemTitle(status.catlgType, item.id)"/>
    <div class="container">
    <header>
      <h2>{{catlgTitle(status.catlgType)}}</h2>
      <item-changed :item="item" :status="status"></item-changed>
    </header>
    </div>
    <catlg-item-control-panel class="catlg-item-control-panel" :item="item" :status.sync="status" :parent="uid"></catlg-item-control-panel>
    <div>
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
  </b-overlay>
  </div>
</template>


<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import CatlgItemMixin from '@/components/Catlg/common/CatlgItemMixin.vue';
import CatlgItemControlPanel from '@/components/Catlg/common/ControlPanel/CatlgItemControlPanel.vue';
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';
import ItemChanged from '@/components/common/ItemChanged.vue';

export default {
  name: 'CatlgDeviceItem',
  components: {
    CatlgWidget,
    CatlgItemControlPanel,
    ItemChanged,
  },

  props: {
    id: String,
    modal: {
      type: Boolean,
      default: false,
    },
  },
  
  mixins: [CatlgItemMixin, CatlgCommon,],
  
  data () {
    return {
      item: {},
      widgetIsValid: {},
      status: {
        itemSaving: false,
        catlgType: 'device',
        modalLocal: this.modal,
      }
    }       
  },

  methods: {
  },

  computed: {
  },
}
   
</script>

<style>
</style>

