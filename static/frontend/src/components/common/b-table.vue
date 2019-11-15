<b-table
      striped 
      hover
      small
      bordered
      sort-null-last
      primary-key="id"
      :sort-compare="compareTUrowWidget"
      :filter="status.tableFilter"
      sticky-header="calc(100vh  - 180px)"
      :items="items"
      :fields="[
        {key: 'deviceType', label: 'Тип', sortable: true, sortByFormatted: false, filterByFormatted: true,
          formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'nomenclature', label: 'Наименование', sortable: true, sortByFormatted: true, filterByFormatted: true,
          formatter: (value, key) => {return GETcatlgItemLabel(key, value)}
        },
        {key: 'serial_num', label: 'Серийный номер', sortable: true},
        {key: 'inv_num', label: 'Инвентарный номер', sortable: true},
        {key: 'comment', label: ' Комментарий', sortable: true},
      ]"
    >
    </b-table>