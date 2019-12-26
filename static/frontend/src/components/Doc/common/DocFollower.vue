<template>
  <div>
  <b-modal id='doc-follower' ok-only title='Иерархия документов'>
  <b-list-group>
    <b-list-group-item v-if="leader"
    class="doc-item-title"
    :to="{name: 'doc.item', params: {docType: leader.docType, id: leader.docId}}"
    target="_blank">
        {{docItemTitle(leader.docType, leader.docId)}}
    </b-list-group-item>

    <b-list-group-item 
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
import {aliases} from '@/components/common/aliases.js';
import { mapActions } from 'vuex';
import Common from '@/components/common/Common.vue';


export default {
  name: 'DocFollower',
  
  components: {
    DocFollowerItem: () => import('@/components/Doc/common/DocFollowerItem.vue'),
  },

  mixins: [Common],
  
  props: {
    docId: Number,
    docType: String,
    showCurrentDoc: {
      type: Boolean,
      default: false,
    },
  },
  
 
  data () {
    return {
      docAlias: aliases.docAlias,
      followers: [],
      leader: null,
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
  },
  
  async mounted() {
    const vm = this
    vm.followers = await vm.docFollower([vm.docType, vm.docId])
    vm.leader = await vm.docLeader([vm.docType, vm.docId])
  },

  created: function() {
  }, 

}
   



</script>

<style scoped>
.doc-item-title {
  text-align: left; 
  max-width: 500px; 
}
</style>

