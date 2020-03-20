<template>
  <div>
    <b-container class="text-right" style="margin-left: 0px; padding-left: 0px">
      <b-row align-v="end">
        <b-col align="left">
          <b-button variant="light" size="sm" @click="editCatlgItemModal(status.catlgType, 'new', `catlg-item-modal-${status.catlgType}-list`)">Добавить</b-button>
          <b-button variant="light" size="sm" @click="onDelCatlgs()">Удалить</b-button>
          <b-button variant="light" size="sm" @click="editCatlgItemModal(status.catlgType, status.selected, `catlg-item-modal-${status.catlgType}-list`)">Редактировать</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
var _ = require('lodash');


export default {
  name: 'CatlgListControlPanel',
  components: {
  },
  mixins: [CatlgCommon],
  props: {
    selected: Array,
    status: Object,
  },

  data () {
    return {
      searchText: "",
    }
  },
  methods: {
    onDelCatlgs: function() {
      const vm = this
      vm.delCatlgs(vm.status, vm.status.selected, vm.status.modal)
      let statusLocal = _.cloneDeep(vm.status)
      statusLocal.selected = []
      vm.$emit('update:status', statusLocal)
    },
  },

  computed: {
    catlgType: function() {
      return this.status.catlgType
    }
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>

<style scoped>
.col {
  max-width: 350px;
}
</style>