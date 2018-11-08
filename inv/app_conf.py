from inv.models import *
from inv.forms import *

DOCUMENT = {
    'income': {'model': DocIncome, 'table_unit': DocIncomeTableUnit, 'form': DocIncomeForm, 'formset': DocIncomeTableUnitFormSet},
    'writeoff': {'model': DocWriteoff, 'table_unit': DocWriteoffTableUnit, 'form': DocWriteoffForm, 'formset': DocWriteoffTableUnitFormSet},
    'move': {'model': DocMove, 'table_unit': DocMoveTableUnit, 'form': DocMoveForm, 'formset': DocMoveTableUnitFormSet},
}

CATALOG = {
    'device': {'model': Device, 'form': DeviceForm, 'order_by': 'name'},
    'devicetype': {'model': DeviceType, 'form': DeviceTypeForm, 'order_by': 'name'},
    'nomenclature': {'model': Nomenclature, 'form': NomenclatureForm, 'order_by': 'name'},
    'person': {'model': Person, 'form': PersonForm, 'order_by': 'surname'},
    'department': {'model': Department, 'form': DepartmentForm, 'order_by': 'name'},
    'stock': {'model': Stock, 'form': StockForm, 'order_by': 'name'},
}

REGISTRY = {
    'devicestock': {'model': RegDeviceStock, 'form': RegDeviceStockForm},
}

OPERATION_DESCR = {
    'reg_write': 'Проведение документа',
    'reg_delete': 'Отмена проведения документа',
    'doc_write': 'Запись документа',
    'catlg_write': 'Запись',
}
