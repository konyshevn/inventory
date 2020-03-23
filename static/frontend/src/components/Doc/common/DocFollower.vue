<template>
  <div>
  <b-modal id='doc-follower' ok-only title='Иерархия документов'>
  <b-list-group >
    <b-list-group-item v-if="!isLeaderEmpty"
    class="doc-item-title"
    :to="{name: 'doc.item', params: {docType: leader.docType, id: leader.docId}}"
    target="_blank">
        {{docItemTitle(leader.docType, leader.docId)}}
    </b-list-group-item>

    <b-list-group-item v-if="docType && docId" 
    class="doc-item-title"
    :style="currentDocStyle"
    :to="{name: 'doc.item', params: {docType: docType, id: docId}}">
        {{docItemTitle(docType, docId)}}
    </b-list-group-item>

    <doc-follower-item v-for="(follower, index) in followers" :key="index"
    :docType="follower.docType" :docId="follower.docId"
    :padd="currentDocPadd + 25"
    >
    </doc-follower-item>
    </b-list-group>
  </b-modal>
  </div>
</template>


<script>
/* eslint-disable no-console */
// import {aliases} from '@/components/common/aliases.js';
import { mapActions } from 'vuex';
import Common from '@/components/common/Common.vue';
import {EventBus} from '@/components/common/event-bus.js'


export default {
  name: 'DocFollower',
  
  components: {
    DocFollowerItem: () => import('@/components/Doc/common/DocFollowerItem.vue'),
  },

  mixins: [Common],
  
  props: {
    docId: String,
    docType: String,
    showCurrentDoc: {
      type: Boolean,
      default: false,
    },
  },
  
 
  data () {
    return {
      // docAlias: aliases.docAlias,
      followers: [],
      leader: {},
      docIdLocal: this.docId,
      docTypeLocal: this.docType,
    }       
  },

  methods: {
    ...mapActions([
      'docFollower',
      'docLeader',
    ])

  },

  computed: {
    currentDocPadd: function() {
      const vm = this
      let padd
      if (vm.leader) {
        padd = 25
      } else {
        padd = 0
      }
      return padd
    },

    currentDocStyle: function() {
      const vm = this
      let style = {
        fontWeight: 'bold',
        textIndent: `${vm.currentDocPadd}px`,
      }
      return style
    },

    isLeaderEmpty: function() {
      const vm = this
      return (Object.keys(vm.leader).length === 0 && vm.leader.constructor === Object)
    },

  },
  
  async mounted() {
    const vm = this
    EventBus.$emit('created-doc-follower', {docType: vm.docType, docId: vm.docId})
    // vm.followers = await vm.docFollower([vm.docType, vm.docId])
    // vm.leader = await vm.docLeader([vm.docType, vm.docId])
  },

  created: function() {
    const vm = this

    EventBus.$on('created-doc-follower', async ({docType, docId}) => {
      if (docType == vm.docType && docId == vm.docId) {
        vm.followers = await vm.docFollower([vm.docType, vm.docId])
        vm.leader = await vm.docLeader([vm.docType, vm.docId])
      }
    })
  }, 

}
   



</script>

<style scoped>
.doc-item-title {
  text-align: left; 
  max-width: 500px; 
}
</style>

