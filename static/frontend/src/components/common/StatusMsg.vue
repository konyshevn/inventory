<template>
  <div class="container">
    <b-modal id="status-msg" size="xl" scrollable title="Сообщения" ok-only>
      <b-list-group  class="text-left">
        <b-list-group-item v-for="(msg, index) in msgs" :key="index">
          {{msg}}
        </b-list-group-item>
      </b-list-group>
    </b-modal>
  </div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {EventBus} from '@/components/common/event-bus.js'

export default {
  name: 'StatusMsg',
  components: {
  },

  props: {
  },

  data () {
    return {
      msgs: []
    }
  },
  methods: {
  },
  mounted: function () {
  },

  created: function () {
    var vm = this
    EventBus.$on('openStatusMsg', msgs => {
      vm.msgs = msgs
      vm.$root.$emit('bv::show::modal', 'status-msg')

    })
  },
  
}
</script>