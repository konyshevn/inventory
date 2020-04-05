<template>
  <div style="padding-left: 20px; padding-right: 20px;">
    <vue-headful :title="`Движения: ${docItemTitle(docType, docId)}`"/>
    <header>
      <h2>{{`Движения: ${docItemTitle(docType, docId)}`}}</h2>
    </header>

    <b-tabs content-class="mt-3">
      <b-tab v-for="registry in registryList" :key="registry"  :title="registry" active>
        <registry-item :registry-name="registry" :doc-type="docType" :doc-id="docId">
        </registry-item>
      </b-tab>
    </b-tabs>

  </div>
</template>


<script>
/* eslint-disable no-console */
import { mapActions } from 'vuex';
import Common from '@/components/common/Common.vue';
import RegistryItem from '@/components/Registry/RegistryItem.vue';

export default {
  name: 'RegistryList',
  components: {
    RegistryItem,
  },

  mixins: [Common],
  
  props: {
    docId: String,
    docType: String,
  },
    
  data () {
    return {
      registryList: [],
    }       
  },

  methods: {
    ...mapActions([
      'FETCHdocItemRegList',
      'FETCHdocItem',
    ])
  },

  computed: {
  },

  async mounted() {
    const vm = this
    await vm.FETCHdocItem([vm.docType, vm.docId])
    let response = await vm.FETCHdocItemRegList([vm.docType, vm.docId])
    if (response.status >= 200 && response.status < 300) {
      vm.registryList = response.data
    }

  },

  created: function() {
  }, 

  beforeDestroy: function() {
  },

}
   

</script>


<style>
header { text-align: left; }
header > h2 { display: inline-block; }
header span { margin-left: 10px;}
</style>

