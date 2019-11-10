<template>
  <div>
    <b-button-group align="left">
      <b-button type="submit" variant="light" size="sm" @click="regWriteDocItem(parent)">Провести</b-button>
      <b-button type="submit" variant="light" size="sm" @click="regDelDocItem(parent)">Отмена проведения</b-button>
      <b-button type="submit" variant="light" size="sm" @click="saveDocItem(parent)">Сохранить</b-button>
      <b-button type="submit" variant="light" size="sm" :disabled="!currentDoc.id" @click="delDocItem()">Удалить</b-button>
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import DocCommon from '@/components/Doc/common/DocCommon.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'DocItemControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
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

  },

  created: function () {
  },
  
}
</script>