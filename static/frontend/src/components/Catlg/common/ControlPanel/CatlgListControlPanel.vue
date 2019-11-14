<template>
  <div>
    <b-container class="text-right" >
      <b-row align-v="end" class="mb-2">
        <b-col align="left">
          <b-button variant="light" size="sm" @click="editCatlgItemModal(catlgType, 'new', `catlg-item-modal-${catlgType}-list`)">Добавить</b-button>
          <b-button variant="light" size="sm" @click="delCatlgs(catlgType, status.selected, status.modal)">Удалить</b-button>
          <b-button variant="light" size="sm" @click="editCatlgItemModal(catlgType, status.selected, `catlg-item-modal-${catlgType}-list`)">Редактировать</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
/* eslint-disable no-console */
import CatlgCommon from '@/components/Catlg/common/CatlgCommon.vue';
var _ = require('lodash');


export default {
  name: 'CatlgListControlPanel',
  components: {
  },
  mixins: [CatlgCommon],
  props: {
    selected: Array,
    status: Object,
  },

  data () {
    return {
      searchText: "",
    }
  },
  methods: {
    tableSearch: function() {
      const vm = this
      //console.log('tableSearch: vm.status.items', vm.status.items)

      let itemsFilter = _.filter(vm.status.items, function(item){
        var findItem = false
        //console.log('tableSearch: item', item)

        for (let key in item) {
          console.log('tableSearch: item.key', item[key])
          //console.log('tableSearch: searchText', vm.searchText)

          if (String(item[key]).indexOf(vm.searchText) >= 0) {findItem = true}
        }
        return findItem
      })
      //console.log('tableSearch: itemsFilter', itemsFilter)
      vm.status.items = itemsFilter
      
    },

    tableSearch2: function() {
      var phrase = this.searchText;
      console.log('phrase: ', phrase)
      var table = document.getElementById(`catlg-list-${this.catlgType}`);
      var regPhrase = new RegExp(phrase, 'i');
      var flag = false;
      for (var i = 1; i < table.rows.length; i++) {
          flag = false;
          for (var j = table.rows[i].cells.length - 1; j >= 1; j--) {
              flag = regPhrase.test(table.rows[i].cells[j].innerHTML);
              if (flag) break;
          }
          if (flag) {
              table.rows[i].style.display = "";
          } else {
              table.rows[i].style.display = "none";
          }

      }
    },


  },
  computed: {
    catlgType: function() {
      return this.status.catlgType
    }
  },
  mounted: function () {
  },

  created: function () {
  },
  
}
</script>

<style scoped>
.col {
  max-width: 350px;
}
</style>