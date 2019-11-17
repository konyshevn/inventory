<template>
  <th @click="sortTable">
    <slot></slot>
    <span>
    </span>
  </th>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'

import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';

export default {
  name: 'SortHeader',
  components: {
  },

  props: {
    field: {
      type: Object,
      default: null,
    },  
  },

  data () {
    return {
    }
  },
  
  computed: {
    ...mapGetters([
      'GETsortStatus',
    ]),
  },
  methods: {
    ...mapMutations([
      'sortObjList',
    ]),

    sortTable: function() {
      const vm = this
      vm.$root.$emit('sort-table', vm.field)
      vm.$root.$emit('switch-sort-order')
    },



  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>

<style scoped>
.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 6px solid black;
}

.arrow.dsc {
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid black;
}
</style>