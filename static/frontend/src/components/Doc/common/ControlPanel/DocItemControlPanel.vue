<template>
  <div>
    <b-button-group align="left" >
      <b-button type="submit" variant="light" size="sm" @click="regWriteDocItem(status, item)">Провести</b-button>
      <b-button type="submit" variant="light" size="sm" @click="regDelDocItem(status, item)">Отмена проведения</b-button>
      <b-button type="submit" variant="light" size="sm" @click="saveDocItem(status, item)">Сохранить</b-button>
      <b-button type="submit" variant="light" size="sm" :disabled="!item.id" @click="delDocItem(status, item)">Удалить</b-button>
      <slot></slot>
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'DocItemControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
    status: Object,
    item: Object,
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
    ]),

  },

  created: function () {
  },
  
}
</script>