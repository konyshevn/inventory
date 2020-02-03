<template>
  <div style="position:relative;display:block">
    <div style="float:left;width:100%">
      <cool-select 
      v-model="modelLocal" 
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
        
        <!-- <template slot="input-start">
          <span v-if="multi" class="input-start">Multi</span>
        </template> -->
        
        <template v-if="!multi" slot="item" slot-scope="{ item }">
          <div class="item">
            <span class="item-name"> {{ item.label }} </span>
          </div>
        </template>

        <template slot="selection" slot-scope="{ item }">
          <div class="selection">
            <span> {{ item.label }} </span>
          </div>
        </template>
        
        <template slot="input-end">
          <b-button v-if="active" size="sm" variant="light" @click="editCatlgItemModal(widgetType, model, catlgItemModalId)"><font-awesome-icon icon="edit"/></b-button>
          <b-button v-if="active" size="sm" variant="light" v-b-modal="modalId"><font-awesome-icon icon="search"/></b-button>
        </template>
      
      </cool-select>
    </div>
    <catlg-widget-modal :parent="uid" :catlgType="widgetType"> </catlg-widget-modal>
    <catlg-item-modal :parent="uid" :catlgType="widgetType"></catlg-item-modal>
  </div>

</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import { mapMutations } from 'vuex';
import { CoolSelect } from 'vue-cool-select';
import CatlgWidgetModal from '@/components/Catlg/common/Widget/CatlgWidgetModal.vue';
import {EventBus} from '@/components/common/event-bus.js'
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';

export default {
  name: 'CatlgWidget',
  components: {
    CatlgItemModal: () => import('@/components/Catlg/common/CatlgItemModal.vue'),
    CoolSelect,
    CatlgWidgetModal,

  },
  mixins: [CatlgCommon],
  props: {
    model: Number,
    widgetType: String,
    required: {
      type: String,
      default: null,
    },
    settings: {
      type: Object,
      default: null,
    },
    modelMulti: {
      type: Array,
      default: () => {return []},
    },
    multi: {
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
      modelLocal: this.model,
    }
  },

  methods: {
    ...mapMutations([
      'SETwidgetState',
      'DELwidgetState',
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

    catlgItemModalId: function () {
      let vm = this
      return `catlg-item-modal-${vm.widgetType}-${vm.uid}`
    },

    uid: function () {
      return String(this._uid)
    },
  },

  watch: {
    model: {
      handler(){
        var vm = this
        vm.modelLocal = vm.model
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
        if (vm.required != null) {
          vm.SETwidgetState([vm.required, vm._uid, vm.isValid])
        }
      },
      immediate: true,
    },

    modelLocal: {
      handler(){
        const vm = this
        vm.$emit('update:model', vm.modelLocal)
      },
    },

  },

  created: function() {
    const vm = this
    EventBus.$on('catlgWidgetSetModel', event => {
      if (event.modalId == vm.modalId){
        vm.$emit('update:model', event.id)
      }
    })
  },


  beforeDestroy: function(){
    var vm = this
    // Костыль. Исправить на удаление uid из списка uid'ов widgetIsValid
    vm.DELwidgetState(vm._uid)
  },

  
}
</script>

<style scoped>
.widget-invalid {
  border: 1px solid red !important;
  border-radius: .25rem !important;
}

</style>