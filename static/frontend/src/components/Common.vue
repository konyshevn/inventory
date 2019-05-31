<template>
  <div>
  </div>
</template>


<script>
/* eslint-disable no-console */
import Vue from 'vue';
import {aliases} from './aliases.js';


export default {
  name: 'Common',
  components: {
  },

  props: {
  },
  
 
  data () {
    return {
    }       
  },

  methods: {
    async confirmMsg (msg='') {
      var vm = this
      var value = await vm.$bvModal.msgBoxConfirm(msg, {
        title: 'Внимание',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'Да',
        cancelTitle: 'Нет',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
      return value
    },

  },

  computed: {
  },
  
  mounted: function () {
  },

  created: function() {
  }, 

}
   



</script>

<style scoped>

</style>

