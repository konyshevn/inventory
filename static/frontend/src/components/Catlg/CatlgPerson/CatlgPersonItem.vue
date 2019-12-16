<template>
  <div class="catlg-person-item container" >
    <div class="container">
    <header>
      <h2>{{catlgTitle(catlgType)}}</h2>
      <b-badge v-if="false" variant="info">редактируется</b-badge> 
    </header>
    </div>
    <catlg-item-control-panel :item="item" :catlgType="catlgType" :parent="uid" style="padding-top: 20px"></catlg-item-control-panel>
    <div style="padding-top: 20px">
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



export default {
  name: 'CatlgPersonItem',
  components: {
    CatlgWidget,
    CatlgItemControlPanel,
  },
  
  props: {
    id: String,
  },
  
  mixins: [CatlgCommon,],
  
  data () {
    return {
      catlgType: 'person',
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
      vm.item = new CatlgConstructor[vm.catlgType]
      //Vue.set(vm, 'item', new CatlgConstructor['device'])
    } else {
      await vm.FETCHcatlgItem([vm.catlgType, vm.id])
      vm.item = vm.GETcatlgItem(vm.catlgType, vm.id)
    }
  },

  created: function() {
  }, 

  beforeDestroy: function() {
    console.log('beforeDestroy')
  },

}
   



</script>

<style scoped>

</style>

