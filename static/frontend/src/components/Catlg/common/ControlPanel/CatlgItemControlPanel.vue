<template>
  <div>
    <b-button-group align="left">
      <b-button type="submit" variant="light" size="sm" @click="saveCatlgItem(item, status, parent)">Сохранить</b-button>
      <b-button type="submit" variant="light" size="sm" :disabled="!item.id" @click="delCatlgs(status, [item.id], modal)">Удалить</b-button>
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';

export default {
  name: 'CatlgItemControlPanel',
  components: {
  },
  mixins: [CatlgCommon],
  props: {
    item: {},
    status: Object,
    parent: null,
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
    modal: function () {
      const vm = this
      if (!(vm.$route.params.catlgType === undefined) && (vm.$route.params.id == vm.item.id)) {
        return false
      } else {
        return true
      }
    },
  },

  created: function () {
  },
  
}
</script>