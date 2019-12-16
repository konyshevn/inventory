<template>
  <div>
    <b-container class="text-right" >
      <b-row align-v="end">
        <b-col align="left">
          <b-button variant="light" size="sm" :to="{path: 'new'}" append>Добавить</b-button>
          <b-button variant="light" size="sm" @click="onDelDocs()">Удалить</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
/* eslint-disable no-console */
import DocCommon from '@/components/Doc/common/DocCommon.vue';
var _ = require('lodash');


export default {
  name: 'DocListControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
    selected: Array,
    status: Object,
  },

  data () {
    return {
    }
  },

  methods: {
    onDelDocs: function() {
      const vm = this
      vm.delDocs(vm.status.docType, vm.status.selected)
      let statusLocal = _.cloneDeep(vm.status)
      statusLocal.selected = []
      vm.$emit('update:status', statusLocal)
    },

  },
  computed: {
    docType: function() {
      return this.$route.params.docType
    }
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>