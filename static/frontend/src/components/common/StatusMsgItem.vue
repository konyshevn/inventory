<template>
  <div>
    <span v-if="isText">{{msg}}</span>
    <span v-else v-for="(section, index) in msg" :key="index">
      <b-link v-if="section.type == 'router-link'" :to="section.settings" target="_blank">
        {{section.data}}
      </b-link>
      <b-link v-if="section.type == 'href-link'" :href="section.settings.url" target="_blank">
        {{section.data}}
      </b-link>
      <span v-if="section.type == 'text'"> 
        {{section.data}}
      </span>
    </span>
  </div>
</template>

<script>
/* eslint-disable no-console */

export default {
  name: 'StatusMsgItem',
  components: {
  },

  props: {
    msg: null,
  },

  data () {
    return {
    }
  },

  methods: {
  },

  computed: {
    isText: function() {
      const vm = this
      return (typeof vm.msg === 'string') ? true : false 
    },
  },

  mounted: function () {
  },

  created: function () {
    // var vm = this
  },
  
}
</script>