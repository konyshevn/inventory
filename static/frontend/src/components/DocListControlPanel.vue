<template>
  <div>
    <b-button-group align="left">
      <b-button variant="light" size="sm" :to="{path: 'new'}" append>Добавить</b-button>
      <b-button variant="light" size="sm" @click="delDocs(docType, status.selected)">Удалить</b-button>
    </b-button-group>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import DocCommon from './DocCommon.vue';
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';


export default {
  name: 'DocListControlPanel',
  components: {
  },
  mixins: [DocCommon],
  props: {
    selected: Array,
    status: Object,
  },

  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
    docType: function() {
      return this.$route.params.docType
    }
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>