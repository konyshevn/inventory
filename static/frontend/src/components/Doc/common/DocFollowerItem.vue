<template>
  <div>

      <b-list-group-item 
      class="doc-item-title"
      :to="{name: 'doc.item', params: {docType: docType, id: docId}}"
      :style="paddStyle" 
      target="_blank"
      >
        {{docItemTitle(docType, docId)}}
      </b-list-group-item>

      <doc-follower-item v-for="(follower, index) in followers" :key="index"
      :docType="follower.docType" :docId="follower.docId"
      :padd="padd+25">
      </doc-follower-item>
  </div>
</template>


<script>
/* eslint-disable no-console */
import {aliases} from '@/components/common/aliases.js';
import { mapActions } from 'vuex';
import Common from '@/components/common/Common.vue';


export default {
  name: 'DocFollowerItem',
  
  components: {
    DocFollowerItem: () => import('@/components/Doc/common/DocFollowerItem.vue'),
  },

  mixins: [Common],
  
  props: {
    docId: Number,
    docType: String,
    padd: {
      type: Number,
      default: 25,
    },
  },
  
 
  data () {
    return {
      docAlias: aliases.docAlias,
      followers: [],
      docIdLocal: this.docId,
      docTypeLocal: this.docType,
    }       
  },

  methods: {
    ...mapActions([
      'docFollower',
    ])

  },

  computed: {
    paddStyle: function () {
      const vm = this
      let style = {
        textIndent: `${vm.padd}px`,
      }
      return style
    },
  },
  
  async mounted() {
    const vm = this
    vm.followers = await vm.docFollower([vm.docType, vm.docId])
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

