<template>
  <div class="catlg-person-item container" >
    <vue-headful :title="catlgItemTitle(catlgType, item.id)"/>
    <div class="container">
    <header>
      <h2>{{catlgTitle(catlgType)}}</h2>
      <b-badge v-if="false" variant="info">редактируется</b-badge> 
    </header>
    </div>
    <catlg-item-control-panel :item="item" :catlgType="catlgType" style="padding-top: 20px"></catlg-item-control-panel>
    <div style="padding-top: 20px">
      <b-table-simple small class="table-borderless" style="width: 500px">
        <tr>
          <td class="align-middle" style="width: 30%">
            Наименование
          </td>
          <td>
            <b-form-input v-model="item.label" type="text"></b-form-input>
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
import * as CatlgConstructor from '@/components/Catlg/common/catlg-constructor.js'



export default {
  name: 'CatlgStockItem',
  components: {
    CatlgItemControlPanel,
  },
  
  props: {
    id: String,
  },
  
  mixins: [CatlgCommon,],
  
  data () {
    return {
      catlgType: 'stock',
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

