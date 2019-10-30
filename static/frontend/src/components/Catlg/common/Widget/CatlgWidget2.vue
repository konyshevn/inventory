<template>
  <div style="position:relative;display:block">
    <div style="float:left;width:100%">
      <cool-select 
      v-model="model" 
      :items="items"
      item-value="id"
      item-text="label"
      :arrowsDisableInstantSelection="true"
      :scrollItemsLimit="10"
      @focus="active=true"
      @blur="active=false"
      :loading="loading"
      disable-filtering-by-search
      @search="onSearch"
      @input="onInput"
      :class="{'widget-invalid': required ? !isValid : false }">
        <template slot="no-data">
          <span>Не найдено</span>
        </template>
        <template slot="item" slot-scope="{ item }">
          <div class="item">
            <span class="item-name"> {{ item.label }} </span>
          </div>
        </template>
        <template slot="input-end">
          <b-button v-if="active" size="sm" variant="light" v-b-modal="modalId">O</b-button>
          <b-button v-if="active" size="sm" variant="light" v-b-modal="modalId">...</b-button>
        </template>
      </cool-select>
    </div>
    <catlg-widget-modal :uid="uid" :catlgType="widgetType"> </catlg-widget-modal>
  </div>

</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import { CoolSelect } from 'vue-cool-select';
import CatlgWidgetModal from '@/components/Catlg/common/Widget/CatlgWidgetModal2.vue';
import {EventBus} from '@/components/common/event-bus.js'

export default {
  name: 'CatlgWidget',
  components: {
    CoolSelect,
    CatlgWidgetModal,
  },
  props: {
    model: Number,
    widgetType: String,
    required: {
      type: Boolean,
      default: false,
    },
  },

  data () {
    return {
      active: false,
      items: [],
      loading: false,
      searchFields: {
        'device': ['nomenclature__label', 'deviceType__label', 'serial_num', 'inv_num'],
        'person': ['name', 'surname'],
        'department': ['label'],
        'stock': ['label']
      },
      isValid: false,
      isInited: false,
      currentItem: Number,

    }
  },

  methods: {
    ...mapMutations([
      'SETcurrentDocWidgetState',
      'DELcurrentDocWidgetState',
    ]),

    onInput: function () {
      var vm = this
      vm.$emit('update:model', vm.model)

    },

    blur: function () {
      var vm=this
      setTimeout(function() { vm.active=false }, 1);
    },



    async onSearch(search) {
      var vm = this
      const lettersLimit = 2;
      Vue.set(vm, 'items', [])
      if (search.length < lettersLimit) {
        Vue.set(vm, 'items', [])
        vm.loading = false;
        return;
      }
      vm.loading = true;
      await vm.$store.dispatch('FETCHcatlg',[vm.widgetType, search, vm.searchFields[vm.widgetType]])
      vm.items = vm.$store.getters.GETcatlgByLabel(vm.widgetType, search)
      vm.loading = false
    },

  },

  mounted: function () {
  },

  computed: {
    modalId: function () {
      let vm = this
      return `modal-${vm.widgetType}-${vm.uid}`
    },

    uid: function () {
      return this._uid
    },
  },

  watch: {
    model: {
      handler(){
        var vm = this
        if (vm.model){
          vm.isValid = true
          if (!vm.isInited){
            vm.items = []
            vm.items.push(vm.$store.getters.GETcatlgItem(vm.widgetType, vm.model))
            vm.isInited = false
          }
        } else {
          vm.isValid = false
        }
        if (vm.required) {
          vm.SETcurrentDocWidgetState([vm._uid, vm.isValid])
        }
      },
      immediate: true,
    }

  },

  created: function() {
    const vm = this
    EventBus.$on('catlgWidgetSetModel', event => {
      if (event.modalId == vm.modalId){
        vm.$emit('update:model', event.id)
      }
    })
  },

  mounted: function() {
  },


  beforeDestroy: function(){
    var vm = this
    // Костыль. Исправить на удаление uid из списка uid'ов widgetIsValid
    vm.DELcurrentDocWidgetState(vm._uid)
  },

  
}
</script>

<style scoped>
.widget-invalid {
  border: 1px solid red !important;
  border-radius: .25rem !important;
}

</style>