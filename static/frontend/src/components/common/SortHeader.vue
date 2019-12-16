<template>
  <th @click="sortTable">
    <slot></slot>
    <span class="arrow" v-if="sortBy == field.key" :class="sortAsc ? 'asc' : 'dsc'">
    </span>
  </th>
</template>

<script>
/* eslint-disable no-console */

export default {
  name: 'SortHeader',
  components: {
  },

  props: {
    field: {
      type: Object,
      default: null,
    },
    sortBy: {
      type: String,
      default: null,
    },
    sortAsc: {
      type: Boolean,
      default: true,
    },  
  },

  data () {
    return {
    }
  },
  
  computed: {
  },

  methods: {
    sortTable: function() {
      const vm = this
      vm.$root.$emit('sort-table', vm.field)
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