<template>
  <div>
    <b-button-group align="left">
      <b-button variant="light" size="sm" :to="{path: 'new'}" append>Добавить</b-button>
      
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
  },

  data () {
    return {
    }
  },
  methods: {
    addDoc: function() {
      const vm = this
      vm.$router.push({ name: 'doc.item', params: {docType: vm.currentDocStatus.docType, id: 'new'}})

    },
    ...mapMutations([
      'DELcurrentDocTUrow',
      'ADDcurrentDocTUrow',
    ]),
  },
  computed: {
    ...mapGetters([
      'currentDocStatus',
    ]),
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>