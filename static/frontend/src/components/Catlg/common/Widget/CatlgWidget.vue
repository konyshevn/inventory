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
      :placeholder="(multi) ? modelMultiSelection : ''"
      :class="{'widget-invalid': required ? !isValid : false }">
        <template slot="no-data">
          <span>Не найдено</span>
        </template>
        
            
        <template slot="item" slot-scope="{ item }">
          <div class="item">
            <span class="item-name"> 
              {{ item.label }}
              <span v-if="modelMultiContains(item.id)" style="float: right;">
                <font-awesome-icon icon="check"/>
              </span>
            </span>
          </div>
        </template>

         <template v-if="multi" slot="selection" >
          <div class="item">
            <span class="item-name" > {{modelMultiSelection}} </span>
          </div>
        </template>


        
        <template slot="input-end">
          <b-button v-if="active" size="sm" variant="light" @click="modelClear()"><font-awesome-icon icon="times"/></b-button>

          <b-button v-if="active && !multi" size="sm" variant="light" @click="editCatlgItemModal(widgetType, model, catlgItemModalId)"><font-awesome-icon icon="edit"/></b-button>

          <b-button v-if="active" size="sm" variant="light" v-b-modal="modalId"><font-awesome-icon icon="search"/></b-button>
          
          <b-button v-if="multi" size="sm" variant="light"
          :disabled="!modelMultiClick"
          v-b-modal="`widget-model-multi-${widgetType}-${uid}`">
              <b-badge>{{modelMultiLength}}</b-badge>
          </b-button>
        </template>


      </cool-select>
    </div>
    <catlg-widget-modal :parent="uid" :catlgType="widgetType"> </catlg-widget-modal>
    <catlg-item-modal :parent="uid" :catlgType="widgetType"></catlg-item-modal>
    
    <b-modal :id="`widget-model-multi-${widgetType}-${uid}`" 
    size="lg" 
    
    ok-only
    :title="catlgTitle(widgetType)">

      <b-list-group style="float: left;">
        <catlg-widget
        :widgetType="widgetType"
        :multi="true"
        :model-multi.sync="modelMulti"
        :model-multi-click="false">
        </catlg-widget>
        <b-list-group-item v-for="id in modelMulti" :key="id">
          <span style="vertical-align: middle;">
            {{GETcatlgItemLabel(widgetType, id)}}
          </span>
          <b-button size="sm" variant="light" style="float: right;"
            @click="modelMultiRemove(id)"
          ><font-awesome-icon icon="times"/>
          </b-button>
        </b-list-group-item>
      </b-list-group>
    </b-modal>
  </div>

</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import { mapMutations } from 'vuex';
import { mapGetters } from 'vuex';
import { CoolSelect } from 'vue-cool-select';
import CatlgWidgetModal from '@/components/Catlg/common/Widget/CatlgWidgetModal.vue';
import {EventBus} from '@/components/common/event-bus.js'
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';

export default {
  name: 'CatlgWidget',
  components: {
    CatlgItemModal: () => import('@/components/Catlg/common/CatlgItemModal.vue'),
    CatlgWidget: () => import('@/components/Catlg/common/Widget/CatlgWidget.vue'),

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
    modelMultiClick: {
      type: Boolean,
      default: true,
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

    modelMultiAdd: function(model) {
      const vm = this
      console.log('modelMultiAdd')
      let modelIndex
      if (model) {
        if (!Array.isArray(vm.modelMulti)){
          vm.$emit('update:model-multi', [model])
          console.log('modelMultiAdd: modelMulti - not array')
        } else {
          modelIndex = vm.modelMulti.indexOf(model)
          if (modelIndex < 0) {
            let newModelMulti = vm.modelMulti
            newModelMulti.push(model)
            vm.$emit('update:model-multi', newModelMulti)
          }
        }
      }
    },

    modelMultiContains: function(model) {
      const vm = this
      console.log('modelMultiContains')
      if (model && vm.modelMulti) {
        let modelIndex = vm.modelMulti.indexOf(model)
        if (modelIndex >= 0 ) {
          return true
        }
      }
      return false
    },

    modelMultiRemove: function(model) {
      const vm = this
      console.log('modelMultiRemove')
      let modelIndex = vm.modelMulti.indexOf(model)
      if ((modelIndex >= 0) && model != null && model != undefined) {
        let newModelMulti = vm.modelMulti
        newModelMulti.splice(modelIndex, 1);
        vm.$emit('update:model-multi', newModelMulti)
      }
    },

    modelClear: function() {
      const vm = this
      vm.$emit('update:model', null)
      if (vm.multi) {
        vm.$emit('update:model-multi', null)
      }
    },
  },

  mounted: function () {
  },

  computed: {
    ...mapGetters([
      'GETcatlgItemLabel',
    ]),

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

    modelMultiLength: function () {
      const vm = this
      let length = 0
      if (Array.isArray(vm.modelMulti)) {
        length = vm.modelMulti.length
      } 
      return length
    },

    modelMultiSelection: function () {
      const vm = this
      let selection = ''
      if (Array.isArray(vm.modelMulti)){
        vm.modelMulti.forEach(function(id, index){
          selection = (index == 0) ? vm.GETcatlgItemLabel(vm.widgetType, id) : selection + '; ' + vm.GETcatlgItemLabel(vm.widgetType, id)
          // selection = selection + '; ' + vm.GETcatlgItemLabel(vm.widgetType, id)
        })
      }
      selection = selection.slice(0, 30) + '...'
      console.log('modelMultiSelection:', selection)
      return selection
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
        vm.modelMultiAdd(vm.modelLocal)
      },
    },

  },

  created: function() {
    const vm = this
    EventBus.$on('catlgWidgetSetModel', event => {
      if (event.modalId == vm.modalId){
        vm.$emit('update:model', event.id)
        vm.modelMultiAdd(event.id)
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