<template>
  <div>
    <b-button-group align="left">
      <b-button variant="light" size="sm" @click="ADDcurrentDocTUrow">Добавить строку</b-button>
      <b-button variant="light" size="sm" @click="DELcurrentDocTUrow">Удалить строку</b-button>
      
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';


export default {
  name: 'TableUnitControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
  },

  data () {
    return {
    }
  },
  methods: {
    ...mapMutations([
      'DELcurrentDocTUrow',
      'ADDcurrentDocTUrow',
    ]),
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>