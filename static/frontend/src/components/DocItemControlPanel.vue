<template>
  <div>
    <b-button-group align="left">
          <b-button type="submit" variant="light" size="sm" @click="regWriteDocItem('docincome', doc)">Провести</b-button>
          <b-button type="submit" variant="light" size="sm" @click="regDelDocItem('docincome', doc)">Отмена проведения</b-button>
          <b-button type="submit" variant="light" size="sm" @click="saveDocItem('docincome', doc)">Сохранить</b-button>
          <b-button type="submit" variant="light" size="sm" @click="delDocItem('docincome', doc)">Удалить</b-button>
        </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import DocCommon from './DocCommon.vue';

export default {
  name: 'DocItemControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
    doc: Object,
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