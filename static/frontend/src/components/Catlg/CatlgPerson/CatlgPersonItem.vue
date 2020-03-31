<template>
  <div class="catlg-person-item container" >
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
      <b-table-simple small class="table-borderless" style="width: 500px" fixed>
        <tr>
          <td class="align-middle" style="width: 30%">
            Фамилия
          </td>
          <td >
            <b-form-input v-model="item.surname" type="text"></b-form-input>
          </td>
        </tr>

        <tr>
          <td class="align-middle">
            Имя
          </td>
          <td>
            <b-form-input v-model="item.name" type="text"></b-form-input>
          </td>
        </tr>
        
        <tr>
          <td class="align-middle">
            Подразделение
          </td>
          <td>
            <catlg-widget widget-type="department" :model.sync="item.department" :required="uid"></catlg-widget>
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
import ItemChanged from '@/components/common/ItemChanged.vue';
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';



export default {
  name: 'CatlgPersonItem',
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
      status: {
        catlgType: 'person',
        itemSaving: false,
        modalLocal: this.modal,
      },
      item: {},
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

