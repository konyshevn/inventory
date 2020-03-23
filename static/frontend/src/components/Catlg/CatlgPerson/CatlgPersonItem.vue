<template>
  <div class="catlg-person-item container" >
    <vue-headful v-if="!modal" :title="catlgItemTitle(status.catlgType, item.id)"/>
    <div class="container">
    <header>
      <h2>{{catlgTitle(status.catlgType)}}</h2>
      <item-changed v-if="item.id" :item-saved.sync="status.itemSaved" :item="item"></item-changed>
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
import ItemChanged from '@/components/common/ItemChanged.vue';



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
  
  mixins: [CatlgCommon,],
  
  data () {
    return {
      status: {
        catlgType: 'person',
        itemSaved: false,
      },
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

   async mounted () {
    var vm = this
    if (vm.id == 'new') {
      vm.item = new CatlgConstructor[vm.status.catlgType]
      //Vue.set(vm, 'item', new CatlgConstructor['device'])
    } else {
      await vm.FETCHcatlgItem([vm.status.catlgType, vm.id])
      vm.item = vm.GETcatlgItem(vm.status.catlgType, vm.id)
    }
  },

  created: function() {
  }, 

  beforeDestroy: function() {
  },

}
   



</script>

<style>
</style>

