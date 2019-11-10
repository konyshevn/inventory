<template>
  <tr v-if="!deleteRow">
    <td class="select-row">
      <b-form-checkbox
      @change.native="UPDcurrentDocTableUnitSelected"
      :value="id"
      >
      </b-form-checkbox>
    </td>
    <td><catlg-widget widget-type="device" :required="parent" :model.sync="device"></catlg-widget></td>
    <td><catlg-widget widget-type="person" :model.sync="person"></catlg-widget></td>
    <td><b-form-input v-model="qty" type="number" number ></b-form-input></td>
    <td><b-form-input v-model="comment" type="text"></b-form-input></td>
  </tr>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import CatlgWidget from '@/components/Catlg/common/Widget/CatlgWidget.vue';

import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';


function mapTwoWayTU (key, getter, mutation) {
  return {
    get () {
      return this.$store.getters[getter][this.index][key]
    },
    set (value) {
      this.$store.commit(mutation, [this.index, key, value])
    }
  }
}

function mapTwoWay (key, getter, mutation) {
  return {
    get () {
      return this.$store.getters[getter][key]
    },
    set (value) {
      this.$store.commit(mutation, [key, value])
    }
  }
}

export default {
  name: 'TableUnitItem',
  components: {
    CatlgWidget,
  },

  props: {
    index: Number,
    parent: null,
  },

  data () {
    return {
      tableUnit:{
        sort:{
          field: "",
          order: -1,
        },
        selected: []
      }
    }
  },
  computed: {
    device: mapTwoWayTU('device', 'currentDocTU', 'UPDcurrentDocTU'),
    person: mapTwoWayTU('person', 'currentDocTU', 'UPDcurrentDocTU'),
    qty: mapTwoWayTU('qty', 'currentDocTU', 'UPDcurrentDocTU'),
    comment: mapTwoWayTU('comment', 'currentDocTU', 'UPDcurrentDocTU'),
    id: mapTwoWayTU('id', 'currentDocTU', 'UPDcurrentDocTU'),
    deleteRow: mapTwoWayTU('DELETE', 'currentDocTU', 'UPDcurrentDocTU'),
    ...mapGetters([
      'currentDocTU',
      
    ])
  },
  methods: {
    ...mapMutations([
      'UPDcurrentDocTU',
      'UPDcurrentDocTableUnitSelected',
    ]),

    ...mapActions([
      'FETCHcurrentDoc'
    ])
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>

<style scoped>

</style>