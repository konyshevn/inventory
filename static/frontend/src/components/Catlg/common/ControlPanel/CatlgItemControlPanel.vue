<template>
  <div>
    <b-button-group align="left">
      <b-button type="submit" variant="light" size="sm" @click="saveCatlgItem(catlgType, item)">Сохранить</b-button>
      <b-button type="submit" variant="light" size="sm" :disabled="!item.id" @click="delCatlgs(catlgType, [item.id])">Удалить</b-button>
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'CatlgItemControlPanel',
  components: {
  },
  mixins: [CatlgCommon],
  props: {
    item: {},
  },

  data () {
    return {
    }
  },
  methods: {
  },
  mounted: function () {
  },
  computed: {
    ...mapGetters([
      'currentDoc',
    ]),
    
    catlgType: function() {
      return this.$route.params.catlgType
    },
  },

  created: function () {
  },
  
}
</script>