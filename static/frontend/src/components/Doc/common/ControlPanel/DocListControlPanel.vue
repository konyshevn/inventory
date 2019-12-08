<template>
  <div>
    <b-container class="text-right" >
      <b-row align-v="end" class="mb-2">
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
import Vue from 'vue'
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
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