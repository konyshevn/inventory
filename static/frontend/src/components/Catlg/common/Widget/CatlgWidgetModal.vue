<template>
  <div >
    <b-modal :id="modalId" size="xl" scrollable
    :title="catlgTitle(catlgType, 'plural')"
    ok-title="Выбрать"
    cancel-title="Отмена" 
    @show="showModal=true" 
    @hidden="showModal=false" 
    @ok="handleOk">
      <catlg-list :modal="modalId" :catlgType="catlgType" v-if="showModal"></catlg-list>
    </b-modal>
    
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgList from '@/components/Catlg/common/CatlgList.vue';
import {aliases} from '@/components/common/aliases.js';
import {EventBus} from '@/components/common/event-bus.js'
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';

export default {
  name: 'CatlgWidgetModal',
  components: {
    CatlgList,
  },
  mixins: [CatlgCommon],
  props: {
    parent: String,
    catlgType: String,
  },

  data () {
    return {
      showModal: false,
      catlgAlias: aliases.catlgAlias,
      selectedItemId: null,
    }
  },
  methods: {
    handleOk: function () {
      const vm = this
      EventBus.$emit('catlgWidgetSetModel', {modalId: vm.modalId, id: vm.selectedItemId})
    },

  },

  computed: {
    modalId: function () {
      let vm = this
      return `modal-${vm.catlgType}-${vm.parent}`
    }
  },

  mounted: function () {
  },

  created: function () {
    var vm = this
    EventBus.$on('modalItemSelected', event => {
      if (event.modalId == vm.modalId) {
        vm.selectedItemId = event.id
        if (event.handleOk) { 
          vm.handleOk()
          vm.$root.$emit('bv::hide::modal', vm.modalId)
        }
      }
    })
  },
  
}
</script>