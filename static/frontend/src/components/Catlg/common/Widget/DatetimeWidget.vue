<template>
  <div>
    <input v-if="!dateOnly" 
    class="form-control"
    v-model="datetime"
    :id="'datetime-widget-' + uid" 
    data-inputmask-alias="datetime" 
    data-inputmask-inputformat="dd.mm.yyyy HH:MM:ss" 
    data-inputmask-placeholder="__.__.____ __:__:__"
    im-insert="false"
    @change="onChange"/>
    <input v-if="dateOnly"
    class="form-control"
    v-model="datetime"
    :id="'datetime-widget-' + uid" 
    data-inputmask-alias="datetime" 
    data-inputmask-inputformat="dd.mm.yyyy" 
    data-inputmask-placeholder="__.__.____"
    im-insert="false"
    @change="onChange" />
  </div>

</template>

<script>
/* eslint-disable no-console */
var Inputmask = require('inputmask');
import moment from 'moment';

export default {
  name: 'DatetimeWidget',
  components: {
  },
  
  mixins: [],
  props: {
    model: String,
    dateOnly: {
      tupe: Boolean,
      default: false,
    }
  },

  data () {
    return {
      datetime: ""
      }
    },

  created: function() {
  },

  methods: {

    onChange: function() {
        console.log('onChange')
        var vm = this
        var newmodel
        if (moment(String(vm.datetime), 'DD.MM.YYYY').isValid() || moment(String(vm.datetime), 'DD.MM.YYYY HH:mm:ss').isValid()) {
          if (vm.dateOnly) {
            newmodel = moment(String(vm.datetime), 'DD.MM.YYYY').format('YYYY-MM-DD')
          } else {
            newmodel = moment(String(vm.datetime), 'DD.MM.YYYY HH:mm:ss').format('YYYY-MM-DDTHH:mm:ssZ')
          }
        } else {
          newmodel = null
          vm.datetime = ""
        }
        vm.$emit('update:model', newmodel)

    },
  },

  watch: {
    model: {
      handler(){
        var vm = this
        if (moment(String(vm.model)).isValid() || moment(String(vm.model)).isValid()) {
          if (vm.dateOnly) {
            vm.datetime = moment(String(vm.model)).format('DD.MM.YYYY')
          } else {
            vm.datetime = moment(String(vm.model)).format('DD.MM.YYYY HH:mm:ss')
          }
        } else {
          vm.datetime = ""
        }
      }
    },
    
  },

  mounted: function () {
    var vm = this
    var selector = document.getElementById("datetime-widget-" + vm.uid);
    var im = new Inputmask({
      "onincomplete": function(){
        var now = moment();
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
        var dtNew
        if (vm.dateOnly){
          dtNew = `${ddNew}.${mmNew}.${yyyyNew}`
          if (dtNew == '..') {
            dtNew = ""
            vm.$emit('update:model', null)
          }
        } else {
          dtNew = `${ddNew}.${mmNew}.${yyyyNew} ${hhNew}:${MMNew}:${ssNew}`
          if (dtNew == '.. ::') {
            dtNew = ""
            //vm.$emit('update:model', now)
          }
        }
        vm.datetime = dtNew
      },

    });
    im.mask(selector);
   },

  computed: {
    uid: function () {
      return String(this._uid)
    },
  },


  
}
</script>