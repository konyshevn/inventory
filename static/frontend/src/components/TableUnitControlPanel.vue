<template>
  <div>
    <b-button-group align="left">
      <b-button variant="light" size="sm" @click="addRowTableUnit('docincome', doc)">Добавить строку</b-button>
      <b-button variant="light" size="sm" @click="deleteRowTableUnit(doc, selected)">Удалить строку</b-button>
      
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import DocCommon from './DocCommon.vue';

export default {
  name: 'TableUnitControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
    doc: Object,
    selected: Array,
  },

  data () {
    return {
    }
  },
  methods: {
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>