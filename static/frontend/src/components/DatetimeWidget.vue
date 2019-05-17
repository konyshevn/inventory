<template>
  <div>
    <input 
    class="form-control"
    v-model="datetime"
    id="datetime-widget" 
    data-inputmask-alias="datetime" 
    data-inputmask-inputformat="dd.mm.yyyy HH:MM:ss" 
    data-inputmask-placeholder="__.__.____ __:__:__"
    im-insert="false"
    @input="onInput" @change="onChange" @update="onUpdate"/>
    <br>
    <br>  
    
    <pre>
      datetime: {{datetime}}
      model: {{model}}
    </pre>
  </div>

</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
var _ = require('lodash');
var Inputmask = require('inputmask');
import moment from 'moment';
//const VueInputMask = require('vue-inputmask').default
//Vue.use(VueInputMask)
import TextMask from 'vue-text-mask'
import MaskedInput from 'vue-masked-input'

export default {
  name: 'DatetimeWidget',
  components: {
    MaskedInput,
    TextMask
  },
  
  mixins: [],
  props: {
    model: String,
  },

  data () {
    return {
      datetime: this.model
      }
    },

  methods: {
    onInput: function(value) {
      var vm = this
      console.log('input ' + value)
    },

    onUpdate: function(value) {
      var vm = this
      console.log('update' + value)
    },

    onChange: function(value) {
      var vm = this
      console.log('change' + value)

    },
  },

  watch: {
    model: {
      immediate: true, 
      handler(newDate, oldDate){
        var vm = this
        console.log('newDate: ', newDate)
        console.log('oldDate: ', oldDate)
        //if (oldDate == "") {
        //  vm.datetime = vm.model
        //}
      }
    }
  },
  
  mounted: function () {
    var vm = this
    var now = moment();
    var selector = document.getElementById("datetime-widget");
    var im = new Inputmask({
      "onincomplete": function(){
        var now = moment();
        console.log('inputmask incomplete ');
        var dd = vm.datetime.slice(0, 2)
        var mm = vm.datetime.slice(3, 5)
        var yyyy = vm.datetime.slice(6, 10)
        var hh = vm.datetime.slice(11, 13)
        var MM = vm.datetime.slice(14, 16)
        var ss = vm.datetime.slice(17, 19)

        var ddNew = ""
        var ddMatch = dd.match(/_/gi)
        if (!ddMatch) {
          ddNew = dd
        } else if (ddMatch.length == 2) {
          ddNew = now.format('DD')
        } else if (dd[0] != 0){
          ddNew = '0' + dd[0]
        } else {
          ddNew = '01'
        }

        var mmNew = ""
        var mmMatch = mm.match(/_/gi)
        if (!mmMatch) {
          mmNew = mm
        } else if (mmMatch.length == 2) {
          mmNew = now.format('MM')
        } else if (mm[0] != 0){
          mmNew = '0' + mm[0]
        } else {
          mmNew = '01'
        }
        
        var yyyyNew = ""
        var yyyyMatch = yyyy.match(/_/gi)
        if (!yyyyMatch) {
          yyyyNew = yyyy
        } else if (yyyyMatch.length == 4) {
          yyyyNew = now.format('YYYY')
        } else if (yyyyMatch.length == 3) {
          yyyyNew = '200' + yyyy[0]
        } else if (yyyyMatch.length == 2) {
          yyyyNew = '20' + yyyy.slice(0, 2)
        } else if (yyyyMatch.length == 1) {
          yyyyNew = '2' + yyyy.slice(0, 3)
        }
        
        var hhNew = ""
        var hhMatch = hh.match(/_/gi)
        if (!hhMatch) {
          hhNew = hh
        } else if (hhMatch.length == 2) {
          hhNew = '00'
        } else {
          hhNew = '0' + hh[0]
        }

        var MMNew = ""
        var MMMatch = MM.match(/_/gi)
        if (!MMMatch) {
          MMNew = MM
        } else if (MMMatch.length == 2) {
          MMNew = '00'
        } else {
          MMNew = '0' + MM[0]
        }

        var ssNew = ""
        var ssMatch = ss.match(/_/gi)
        if (!ssMatch) {
          ssNew = ss
        } else if (ssMatch.length == 2) {
          ssNew = '00'
        } else {
          ssNew = '0' + ss[0]
        }

        var dtNew = `${ddNew}.${mmNew}.${yyyyNew} ${hhNew}:${MMNew}:${ssNew}`
        console.log(dtNew)
        vm.datetime = dtNew
      },

    });
    im.mask(selector);

    //do something
  

   },

  computed: {
  },

  watch: {
  },

  created: function() {
  }
  
}
</script>