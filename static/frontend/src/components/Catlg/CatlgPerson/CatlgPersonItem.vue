<template>
  <div class="catlg-person-item container" >
    <div class="container">
    <header>
      <h2>{{catlgTitle(catlgType)}}</h2>
      <b-badge v-if="false" variant="info">редактируется</b-badge> 
    </header>
    </div>
    <catlg-item-control-panel :item="item" :catlgType="catlgType" :parent="uid"></catlg-item-control-panel>
    <div>
      <b-table-simple small class="table-borderless" style="width: 500px">
        <b-tr>
          <b-td>
            Фамилия
          </b-td>
          <b-td >
            <b-form-input v-model="item.surname" type="text"></b-form-input>
          </b-td>
        </b-tr>

        <b-tr>
          <b-td>
            Имя
          </b-td>
          <b-td>
            <b-form-input v-model="item.name" type="text"></b-form-input>
          </b-td>
        </b-tr>
        
        <b-tr>
          <b-td>
            Подразделение
          </b-td>
          <b-td>
            <catlg-widget widget-type="department" :model.sync="item.department" :required="uid"></catlg-widget>
          </b-td>
        </b-tr>
               
      </b-table-simple>
    </div>

  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import CatlgItemControlPanel from '@/components/Catlg/common/ControlPanel/CatlgItemControlPanel.vue';
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';
import SortHeader from '@/components/common/SortHeader.vue'
import * as CatlgConstructor from '@/components/Catlg/common/catlg-constructor.js'



export default {
  name: 'CatlgPersonItem',
  components: {
    CatlgWidget,
    SortHeader,
    CatlgItemControlPanel,
  },
  
  props: {
    id: Number,
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

