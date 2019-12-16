<template>
  <div>
    <b-button-group align="left">
      <b-button type="submit" variant="light" size="sm" @click="saveCatlgItem(catlgType, item, parent)">Сохранить</b-button>
      <b-button type="submit" variant="light" size="sm" :disabled="!item.id" @click="delCatlgs(catlgType, [item.id], modal)">Удалить</b-button>
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'CatlgItemControlPanel',
  components: {
  },
  mixins: [CatlgCommon],
  props: {
    item: {},
    catlgType: {
      type: String,
      default: '',
    },
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
    ...mapGetters([
      'currentDoc',
    ]),

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