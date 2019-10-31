<template>
  <div class="catlg-person-item container" >
    <div class="container">
    <header>
      <h2 align="left">Подразделение</h2>
      <b-badge v-if="false" variant="info">редактируется</b-badge> 
    </header>
    </div>
    <catlg-item-control-panel :item="item" :catlgType="catlgType"></catlg-item-control-panel>
    <div>
      <b-table-simple small class="table-borderless" style="width: 500px">
        <b-tr>
          <b-td>
            Наименование
          </b-td>
          <b-td >
            <b-form-input v-model="item.label" type="text"></b-form-input>
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
import * as CatlgConstructor from '@/components/Catlg/common/catlg-constructor.js'



export default {
  name: 'CatlgDepartmentItem',
  components: {
    CatlgWidget,
    CatlgItemControlPanel,
  },
  
  props: {
    id: Number,
  },
  
  mixins: [CatlgCommon,],
  
  data () {
    return {
      catlgType: 'department',
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


header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}


</style>

