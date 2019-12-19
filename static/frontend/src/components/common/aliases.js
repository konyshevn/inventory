export const aliases = {
  docAlias: {
    docincome:    {item: 'DocIncomeItem', list: 'DocIncomeList', titleSingular: 'Оприходование', titlePlural: 'Оприходования',
                  fieldsMap: {
                    department: 'department',
                    stock: 'stock',
                    tableUnit: {
                      device: 'device',
                      person: 'person',
                    },
                  },
    },

    docwriteoff:  {item: 'DocWriteoffItem', list: 'DocWriteoffList', titleSingular: 'Списание', titlePlural: 'Списания',
                  fieldsMap: {
                    department: 'department',
                    stock: 'stock',
                    tableUnit: {
                      device: 'device',
                      person: 'person',
                    },
                  },
    },

    docmove:      {item: 'DocMoveItem', list: 'DocMoveList', titleSingular: 'Перемещение', titlePlural: 'Перемещения',
                  fieldsMap: {
                    department_from: 'department',
                    department_to: 'department',
                    stock_from: 'stock',
                    stock_to: 'stock',
                    tableUnit: {
                      device: 'device',
                      person_from: 'person',
                      person_to: 'person',
                    },
                  },
    },

    docinventory: {item: 'DocInventoryItem', list: 'DocInventoryList', titleSingular: 'Инвентаризация', titlePlural: 'Инвентаризации',
                  fieldsMap: {
                    department: 'department',
                    stock: 'stock',
                    tableUnit: {
                      device: 'device',
                      person_accountg: 'person',
                      person_fact: 'person',
                      stock_fact: 'stock',
                    },
                  },
    },
  },
  
  catlgAlias: {
    device:       {item: 'CatlgDeviceItem', list: 'CatlgDeviceList', titleSingular: 'Устройство', titlePlural: 'Устройства',
                  fieldsMap: {},
    },
    
    department:   {item: 'CatlgDepartmentItem', list: 'CatlgDepartmentList', titleSingular: 'Подразделение', titlePlural: 'Подразделения',
                  fieldsMap: {},
    },
    
    stock:        {item: 'CatlgStockItem', list: 'CatlgStockList', titleSingular: 'Склад', titlePlural: 'Склады',
                  fieldsMap: {},
    },

    person:       {item: 'CatlgPersonItem', list: 'CatlgPersonList', titleSingular: 'Сотрудник', titlePlural: 'Сотрудники',
                  fieldsMap: {},
    },

    deviceType:   {item: 'CatlgDeviceTypeItem', list: 'CatlgDeviceTypeList', titleSingular: 'Тип устройства', titlePlural: 'Типы устройств',
                  fieldsMap: {},
    },

    nomenclature: {item: 'CatlgNomenclatureItem', list: 'CatlgNomenclatureList', titleSingular: 'Номенклатура', titlePlural: 'Номенклатура',
                  fieldsMap: {},
    },

  }

}